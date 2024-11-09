import re
import logging

from olvid import datatypes, listeners, OlvidClient

from ClientHolder import ClientHolder, ClientWrapper
from utils import send_message_wait_and_check_content, send_message_with_attachments_in_memory_and_check


def compare_message_lists(given: list[datatypes.Message], expected: list[datatypes.Message]):
	given = sorted(given, key=message_sort_key)
	expected = sorted(expected, key=message_sort_key)
	assert len(given) == len(expected), f"Invalid list length: {len(given)} != {len(expected)}\ngiven:{given}\nexpected: {expected}"
	for i in range(len(given)):
		assert given[i] == expected[i], f"Invalid element in list: {given[i]} != {expected[i]}\ngiven:{given}\nexpected: {expected}"


def message_sort_key(m: datatypes.Message):
	return m.id.id if m.id.type == datatypes.MessageId.Type.TYPE_INBOUND else -1 * m.id.id


async def test_filtering_discussion(c1: ClientWrapper, c2: ClientWrapper):
	# create discussions
	created_groups: list[datatypes.Group] = [
		await c1.group_new_standard_group(name="GROUP-NAME"),
		await c1.group_new_standard_group(name="MyNameIs1"),
		await c1.group_new_standard_group(name="MyNameIs2"),
	]

	all_discussions: list[datatypes.Discussion] = sorted([d async for d in c1.discussion_list()], key=lambda d: d.id)

	# delete created discussions
	for group in created_groups:
		await c1.group_disband(group_id=group.id)


async def test_filtering_invitation(c1: ClientWrapper, c2: ClientWrapper):
	invitations: list[datatypes.Invitation] = [i async for i in c1.invitation_list(datatypes.InvitationFilter(type=datatypes.InvitationFilter.Type.TYPE_INTRODUCTION))]


async def test_filtering_messages(c1: ClientWrapper, c2: ClientWrapper):
	contact_1, contact_2 = await c1.get_contact_associated_to_another_client(c2), await c1.get_contact_associated_to_another_client(c2)

	# create messages
	await send_message_wait_and_check_content(c1, c2, "Hello there")
	await send_message_wait_and_check_content(c1, c2, "my body is 1")
	message_to_react_to_1, _ = await send_message_wait_and_check_content(c1, c2, "Please react to me")
	_, message_to_react_to_2 = await send_message_wait_and_check_content(c1, c2, "I want reactions too")
	message_to_reply_to, _ = await send_message_wait_and_check_content(c1, c2, "MY body is 2")
	await send_message_wait_and_check_content(c1, c2, "This message embed a reply", replied_message_id=message_to_reply_to.id)
	await send_message_with_attachments_in_memory_and_check(c1, c2, body="", filenames=["file.txt", "image.jpg"], file_contents=[b"a", b"d"])
	await send_message_with_attachments_in_memory_and_check(c1, c2, body="Film and image", filenames=["film.mp4", "image.jpg"], file_contents=[b"a", b"d"])

	# send reactions
	# add bot for reactions
	bots: list[OlvidClient] = [
		c1.create_notification_bot(listeners.MessageReactionAddedListener(handler=lambda m, r: m, count=2)),
		c2.create_notification_bot(listeners.MessageReactionAddedListener(handler=lambda m, r: m, count=2)),

		# TODO re-enable when notification filtering implemented
		# c1.create_notification_bot(listeners.MessageReactionAddedListener(handler=lambda m, r: m, count=1, filter=datatypes.MessageFilter(reacted_by_me=True, reaction="🌍"))),
		# c2.create_notification_bot(listeners.MessageReactionAddedListener(handler=lambda m, r: m, count=1, filter=datatypes.MessageFilter(reacted_by_contact_id=contact_2.id, reaction="🌍"))),
		# c1.create_notification_bot(listeners.MessageReactionAddedListener(handler=lambda m, r: m, count=1, filter=datatypes.MessageFilter(reacted_by_contact_id=contact_1.id, reaction="🪦"))),
		# c2.create_notification_bot(listeners.MessageReactionAddedListener(handler=lambda m, r: m, count=1, filter=datatypes.MessageFilter(reacted_by_me=True, reaction="🪦"))),
	]
	await message_to_react_to_1.react("🌍")
	await message_to_react_to_2.react("🪦")

	for bot in bots:
		await bot.wait_for_listeners_end()

	####
	# start tests
	####
	all_messages_1: list[datatypes.Message] = sorted([m async for m in c1.message_list()], key=message_sort_key)
	all_messages_2: list[datatypes.Message] = sorted([m async for m in c2.message_list()], key=message_sort_key)

	# no filter
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter()
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1])

	# body search
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(body_search="body")
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if re.findall(r"body", m.body)])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(body_search="nothing you can find in a body")
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if re.findall(r"nothing you can find in a body", m.body)])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(body_search="^my")
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if re.findall(r"^my", m.body)])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(body_search="")
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if re.findall(r"", m.body)])

	# location
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(location=datatypes.MessageFilter.Location.LOCATION_HAVE)
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if m.message_location])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(location=datatypes.MessageFilter.Location.LOCATION_HAVE_NOT)
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if not m.message_location])

	# reply
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(do_not_reply_to_a_message=True)
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if not m.replied_message_id])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(reply_to_a_message=True)
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if m.replied_message_id])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(replied_message_id=message_to_reply_to.id)
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if m.replied_message_id == message_to_reply_to.id])
	message_filter: datatypes.MessageFilter = datatypes.MessageFilter(replied_message_id=message_to_react_to_1.id)
	compare_message_lists([m async for m in c1.message_list(filter=message_filter)], [m for m in all_messages_1 if m.replied_message_id == message_to_react_to_1.id])

	# reactions
	# noinspection PyShadowingBuiltins
	async def test_reaction(client: ClientWrapper, other_client_contact_id: int, all_messages: list[datatypes.Message]):
		# reaction
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reaction=datatypes.MessageFilter.Reaction.REACTION_HAS)
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reaction=datatypes.MessageFilter.Reaction.REACTION_HAS_NOT)
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions]) == 0])

		# reaction filters
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="🌍")])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "🌍"]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="🌍", reacted_by_me=True)])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "🌍" and r.contact_id == 0]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="🪦")])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "🪦"]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="🪦", reacted_by_contact_id=other_client_contact_id)])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "🪦" and r.contact_id == other_client_contact_id]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="💣")])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "💣"]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="💣", reacted_by_me=True)])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "💣" and r.contact_id == 0]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reaction="💣", reacted_by_contact_id=other_client_contact_id)])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.reaction == "💣" and r.contact_id == other_client_contact_id]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reacted_by_me=True)])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.contact_id == 0]) > 0])
		filter: datatypes.MessageFilter = datatypes.MessageFilter(reactions_filter=[datatypes.ReactionFilter(reacted_by_contact_id=other_client_contact_id)])
		compare_message_lists([m async for m in client.message_list(filter=filter)], [m for m in all_messages if len([r for r in m.reactions if r.contact_id == other_client_contact_id]) > 0])

	await test_reaction(c1, contact_1.id, all_messages_1)
	await test_reaction(c2, contact_2.id, all_messages_2)


async def test_filtering(client_holder: ClientHolder, fast_mode=False):
	for c1, c2 in client_holder.get_all_client_pairs():
		logging.info(f"{c1.identity.id} <-> {c2.identity.id}: message filtering")
		await test_filtering_messages(c1, c2)
