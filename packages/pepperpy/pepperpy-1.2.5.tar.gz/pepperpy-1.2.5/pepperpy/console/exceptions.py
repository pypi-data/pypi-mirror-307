from ..core.exceptions import ConsoleError


class ConsoleDisplayError(ConsoleError):
    """Erro ao exibir dados no console"""

    pass


class ConsoleInputError(ConsoleError):
    """Erro durante entrada de dados"""

    pass


class ConsoleFileError(ConsoleError):
    """Erro em operações com arquivos"""

    pass
