import streamlit as st
from IPython.display import display
from solidipes.loaders.data_container import DataContainer
from solidipes.utils import solidipes_logging as logging
from solidipes.viewers import backends as viewer_backends
from solidipes.viewers.viewer import Viewer

print = logging.invalidPrint
logger = logging.getLogger()


class Binary(Viewer):
    """Viewer for (unknown) binary"""

    def __init__(self, data=None):
        self.data = []
        super().__init__(data)

    def add(self, data_container):
        """Append text to the viewer"""
        self.check_data_compatibility(data_container)

        if isinstance(data_container, DataContainer):
            self.data.append(data_container.file_info)
        else:
            raise RuntimeError("can only handle binary types")

    def show(self):
        if viewer_backends.current_backend == "jupyter notebook":
            for d in self.data:
                for k, v in d.data.items():
                    display(k, v)

        elif viewer_backends.current_backend == "streamlit":
            with st.container():
                logger.info(self.data)
                for d in self.data:
                    for k, v in d.data.items():
                        st.markdown(f"- {k} : {v}")
        else:  # python
            for d in self.data:
                for k, v in d.data:
                    logger.info(k, k)
