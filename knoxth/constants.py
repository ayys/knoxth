"""
Specifies the valid permissions for any scope.

from knoxth.constants import ACCESS, MODIFY, DELETE

ACCESS - Must have this permission for SAFE_METHODS (GET, HEAD, OPTIONS)
MODIFY - Must have this permission for POST and PUT methods
DELETE - Must have this permission for DELETE method
"""
ACCESS = 1 << 1
MODIFY = 1 << 2
DELETE = 1 << 3

PERMISSIONS = (ACCESS, MODIFY, DELETE)

ALL_PERMISSIONS = ACCESS | MODIFY | DELETE
