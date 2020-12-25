class BadRequest(Exception):
    pass


class ResourceNotFound(Exception):
	pass


class UnprocessableEntity(Exception):
	pass


class InternalError(Exception):
	pass


error_messages = {
	"BadRequest": {
		"success": False,
		"message": "Bad Request",
		"status_code": 400
    },
    "ResourceNotFound": {
		"success": False,
		"message": "Resource Not Found",
		"status_code": 404
    },
    "UnprocessableEntity": {
		"success": False,
		"message": "Unprocessable Entity",
		"status_code": 422
    },
    "InternalError": {
		"success": False,
		"message": "Internal Error",
		"status_code": 500
    }
}