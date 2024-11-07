"""Our own Python bindings to the vis.js library in JavaScript."""

import IPython.display as ipd
import ipywidgets as widgets
import html
import stormvogel.displayable
import stormvogel.html_templates
import stormvogel.communication_server
import json
import random
import string
import logging

spam: widgets.Output = widgets.Output()


class Network(stormvogel.displayable.Displayable):
    EXTRA_PIXELS: int = 20  # To prevent the scroll bar around the Network.

    def __init__(
        self,
        name: str | None = None,
        width: int = 800,
        height: int = 600,
        output: widgets.Output | None = None,
        do_display: bool = True,
        debug_output: widgets.Output = widgets.Output(),
        do_init_server: bool = True,
    ) -> None:
        """Display a visjs network using IPython. The network can display by itself or you can specify an Output widget in which it should be displayed.

        Args:
            name (str): Used to name the iframe. ONLY SPECIFY IF YOU KNOW WHAT YOU ARE DOING. You should never create two networks with the same name, they might clash.
            width (int): Width of the network, in pixels.
            height (int): Height of the network, in pixels.
            output (widgets.Output): An output widget within which the network should be displayed.
            do_display (bool): Set to true iff you want the Network to display. Defaults to True.
            debug_output (widgets.Output): Debug information is displayed in this output. Leave to default if that doesn't interest you."""
        super().__init__(output, do_display, debug_output)
        if name is None:
            self.name: str = "".join(random.choices(string.ascii_letters, k=10))
        else:
            self.name: str = name
        self.width: int = width
        self.height: int = height
        self.nodes_js: str = ""
        self.edges_js: str = ""
        self.options_js: str = "{}"
        self.new_nodes_hidden: bool = False
        if do_init_server:
            self.server: stormvogel.communication_server.CommunicationServer = (
                stormvogel.communication_server.initialize_server()
            )
        # Note that this refers to the same server as the global variable in stormvogel.communication_server.

    def enable_exploration_mode(self, initial_node_id: int):
        """Every node becomes invisible. You can then click any node to reveal all of its successors. Call before adding any nodes to the network."""
        self.new_nodes_hidden = True
        self.initial_node_id = initial_node_id

    def update_exploration_mode(self, initial_node_id: int):
        # Make all nodes invisible.
        ipd.display(
            ipd.Javascript(
                f"document.getElementById('{self.name}').contentWindow.makeAllNodesInvisible()"
            )
        )
        # Make the initial state visible.
        ipd.display(
            ipd.Javascript(
                f"document.getElementById('{self.name}').contentWindow.makeNodeVisible({initial_node_id})"
            )
        )
        # All future nodes to be added will be hidden as well.

    def get_positions(self) -> dict:
        """Get the current positions of the nodes on the canvas. Returns empty dict if unsucessful.
        Example result: {"0": {"x": 5, "y": 10}}"""
        if self.server is None:
            with self.debug_output:
                logging.warning(
                    "Server not initialized. Could not retrieve position data."
                )
            raise TimeoutError("Server not initialized.")
        try:
            positions: dict = json.loads(
                self.server.request(
                    f"""JSON.stringify(document.getElementById('{self.name}').contentWindow.network.getPositions())"""
                )
            )
            return positions
        except TimeoutError:
            with self.debug_output:
                logging.warning("Timed out. Could not retrieve position data.")
            raise TimeoutError("Timed out. Could not retrieve position data.")

    def add_node(
        self,
        id: int,
        label: str | None = None,
        group: str | None = None,
        position_dict: dict | None = None,
    ) -> None:
        """Add a node. Only use before calling show."""
        current = "{ id: " + str(id)
        if label is not None:
            current += f", label: `{label}`"
        if group is not None:
            current += f', group: "{group}"'
        if position_dict is not None and str(id) in position_dict:
            current += (
                f', x: {position_dict[str(id)]["x"]}, y: {position_dict[str(id)]["y"]}'
            )
        if self.new_nodes_hidden and id != self.initial_node_id:
            current += ", hidden: true"
        current += " },\n"
        self.nodes_js += current

    def add_edge(
        self,
        from_: int,
        to: int,
        label: str | None = None,
    ) -> None:
        """Add an edge. Only use before calling show."""
        current = "{ from: " + str(from_) + ", to: " + str(to)
        if label is not None:
            current += f', label: "{label}"'
        current += " },\n"
        self.edges_js += current

    def set_options(self, options: str) -> None:
        """Set the options. Only use before calling show."""
        self.options_js = options

    def generate_html(self) -> str:
        """Generate the html for the network."""
        js = (
            f"""
        var nodes = new vis.DataSet([{self.nodes_js}]);
        var edges = new vis.DataSet([{self.edges_js}]);
        var options = {self.options_js};
        """
            + stormvogel.html_templates.NETWORK_JS
        )

        sizes = f"""
        width: {self.width}px;
        height: {self.height}px;
        border: 1px solid lightgray;
        """

        html = stormvogel.html_templates.START_HTML.replace(
            "__JAVASCRIPT__", js
        ).replace("__SIZES__", sizes)
        return html

    def generate_iframe(self) -> str:
        """Generate an iframe for the network, using the html."""
        return f"""
          <iframe
                id="{self.name}"
                width="{self.width + self.EXTRA_PIXELS}"
                height="{self.height + self.EXTRA_PIXELS}"
                frameborder="0"
                srcdoc="{html.escape(self.generate_html())}"
                border:none !important;
                allowfullscreen webkitallowfullscreen mozallowfullscreen
          ></iframe>"""

    def show(self) -> None:
        """Display the network on the output that was specified at initialization, otherwise simply display it."""
        iframe = self.generate_iframe()
        with self.output:  # Display the iframe within the Output.
            ipd.clear_output()
            ipd.display(widgets.HTML(iframe))
        self.maybe_display_output()
        with self.debug_output:
            logging.info("Called Network.show")

    def reload(self) -> None:
        """Tries to reload an existing visualization (so it uses a modified layout). If show was not called before, nothing happens."""
        iframe = self.generate_iframe()
        with self.output:
            ipd.clear_output()
            ipd.display(widgets.HTML(iframe))
        with self.debug_output:
            logging.info("Called Network.reload")

    def update_options(self, options: str):
        """Update the options. The string DOES NOT WORK if it starts with 'var options = '"""
        self.set_options(options)
        js = f"""document.getElementById('{self.name}').contentWindow.network.setOptions({options});"""
        with self.spam:
            ipd.display(ipd.Javascript(js))
        self.spam_side_effects()

        with self.debug_output:
            logging.info("The previous javascript error is no problem in most cases.")
        with self.debug_output:
            logging.info("Called Network.update_options")

    def clear(self) -> None:
        """Clear the output."""
        with self.output:
            ipd.clear_output()
