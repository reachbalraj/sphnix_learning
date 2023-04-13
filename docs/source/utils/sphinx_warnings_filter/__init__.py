__version__ = "0.2.3"

from .warnings_filter import configure


def setup(app):
    """Setups up the extension."""
    app.add_config_value("warnings_filter_config", "", "")

    app.connect("builder-inited", configure)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }