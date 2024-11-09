import asyncio
import base64
import logging
import random
import string
from os import remove

import grpc.aio

from ClientHolder import ClientHolder, ClientWrapper
from olvid import datatypes

PNG_IMAGE_AS_B64 = "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"


# noinspection PyProtectedMember
async def create_identities(client_holder: ClientHolder, number_of_identities: int):
	#####
	# Create identities
	#####
	random_prefix = "".join(random.choice(string.ascii_letters) for _ in range(5))
	for i in range(number_of_identities):
		first_name = f"TestIdentity-{random_prefix}"
		last_name = str(i)
		position = "TO DEL"
		company = "Earth"
		identity = await client_holder.create_identity(first_name=first_name, last_name=last_name, position=position, company=company)
		expected_identity = datatypes.Identity(details=datatypes.IdentityDetails(first_name=first_name, last_name=last_name, position=position, company=company), display_name=f"{first_name} {last_name} ({position} @ {company})", keycloak_managed=False)
		assert identity._test_assertion(expected_identity)

	#####
	# Show created identities
	#####
	for client in client_holder.clients:
		logging.info(f"{client.identity.id}: {client.identity.details.first_name} {client.identity.details.last_name}")

	#####
	# Check admin identity get commands
	#####
	for client in client_holder.clients:
		assert client.identity == await client_holder.admin_client.admin_identity_admin_get(client.identity.id)
		assert await client.identity_get() == await client_holder.admin_client.admin_identity_admin_get(client.identity.id)


async def set_and_unset_identity_photo(client: ClientWrapper):
	# file that does not exist
	try:
		await client.identity_set_photo("this_file_does_not_exists.txt")
		raise Exception(f"Do not detected invalid file")
	except IOError:
		pass
	except Exception as e:
		print(type(e))
		raise Exception(f"Invalid exception raised: {e}")
	# check image is set (wait for DbCache to be up-to-date ...)
	await asyncio.sleep(0.1)
	assert not (await client.identity_get()).has_a_photo

	# valid filename, invalid payload
	try:
		with open("invalid_photo.png", "w") as fd:
			fd.write("This is not a photo !" * 20)
		await client.identity_set_photo("invalid_photo.png")
		raise Exception(f"Daemon accepted an invalid format image")
	except grpc.aio.AioRpcError:
		pass
	except Exception as e:
		raise Exception(f"Invalid exception raised: {e}")
	finally:
		remove("invalid_photo.png")
	# check image is set (wait for DbCache to be up-to-date ...)
	await asyncio.sleep(0.1)
	assert not (await client.identity_get()).has_a_photo

	# valid image
	with open("image.png", "wb") as fd:
		fd.write(base64.b64decode(PNG_IMAGE_AS_B64))
	await client.identity_set_photo("image.png")

	# check image is set (wait for DbCache to be up-to-date ...)
	await asyncio.sleep(0.1)
	assert (await client.identity_get()).has_a_photo

	# unset image
	await client.identity_remove_photo()

	# delete file on disk
	remove("image.png")


async def test_identity(client_holder: ClientHolder, number_of_identities: int):
	await create_identities(client_holder, number_of_identities)

	for client in client_holder.clients:
		await set_and_unset_identity_photo(client)
