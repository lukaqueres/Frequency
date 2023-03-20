class InvalidLocalisationError(ValueError):
	pass


class DiscordLocalisationNotSupportedError(TypeError):
	pass


class TranslationNotFoundError(KeyError):
	pass
