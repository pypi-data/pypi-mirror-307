from typing import Any, Dict, Optional


class ValidationError(Exception):
    pass


class ErrorExtra:
    conflict_user_id: str

    def __init__(self, conflict_user_id: str):
        self.conflict_user_id = conflict_user_id

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'conflict_user_id': self.conflict_user_id}
        return data

    @classmethod
    def new(cls, json: Dict[str, Any]):
        return cls(conflict_user_id=json['conflict_user_id'])


class ApiError(Exception):
    status: int
    message: str
    code: Optional[str] = None
    reason: Optional[str] = None
    extra: Optional[ErrorExtra] = None

    def __init__(
        self,
        status: int,
        message: str,
        code: Optional[str] = None,
        reason: Optional[str] = None,
        details: Optional[Dict[str, str]] = None,
        extra: Optional[ErrorExtra] = None,
    ):
        self.status = status
        self.message = message
        self.code = code
        self.reason = reason
        self.details = details
        self.extra = extra

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {'status': self.status, 'message': self.message}
        if self.code is not None:
            data['code'] = self.code
        if self.reason is not None:
            data['reason'] = self.reason
        if self.details is not None:
            data['details'] = self.details
        if self.extra is not None:
            data['extra'] = self.extra.serialize()

        return data

    @classmethod
    def new(cls, status: int, json: Dict[str, Any]):
        extra = None
        if 'extra' in json:
            extra = ErrorExtra.new(json['extra'])

        return cls(
            status=status,
            message=json['message'],
            code=json.get('code'),
            reason=json.get('reason'),
            details=json.get('details'),
            extra=extra,
        )
