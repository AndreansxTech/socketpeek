from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, Label
from textual.containers import Container, Grid, Vertical
from .utils import check_port, validate_port

class SocketPeekApp(App):
    CSS = """
    #main-container {
        width: 100%;
        height: 100%;
        padding: 2 4;
    }
    
    #input-form {
        margin-bottom: 2;
        border: solid gray;
        padding: 1;
        background: #252525;
    }
    
    #form-title {
        text-align: center;
        background: #353535;
        padding: 1;
        width: 100%;
        margin-bottom: 1;
    }
    
    .input-container {
        width: 100%;
        margin-bottom: 1;
    }
    
    .input-label {
        width: 20%;
        padding-top: 1;
    }
    
    .input-field {
        width: 80%;
    }
    
    #button-container {
        margin-top: 1;
        text-align: center;
    }
    
    #result-area {
        border: solid gray;
        padding: 1;
        height: auto;
        background: #252525;
    }
    
    #result-title {
        text-align: center;
        background: #353535;
        padding: 1;
        width: 100%;
        margin-bottom: 1;
    }
    
    #result-content {
        margin: 1;
        padding: 1;
        min-height: 3;
    }
    
    .success {
        color: green;
    }
    
    .error {
        color: red;
    }
    
    .info {
        color: blue;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            with Vertical(id="input-form"):
                yield Label("Socket Connection Checker", id="form-title")
                
                with Grid(id="host-row", classes="input-container"):
                    yield Label("Host:", classes="input-label")
                    yield Input(placeholder="Enter hostname or IP (e.g. google.com)", id="host-input", classes="input-field")
                
                with Grid(id="port-row", classes="input-container"):
                    yield Label("Port:", classes="input-label")
                    yield Input(placeholder="Enter port number (1-65535)", id="port-input", classes="input-field")
                
                with Grid(id="timeout-row", classes="input-container"):
                    yield Label("Timeout:", classes="input-label")
                    yield Input(placeholder="Connection timeout in seconds", value="3.0", id="timeout-input", classes="input-field")
                
                with Container(id="button-container"):
                    yield Button("Check Connection", variant="primary", id="check-button")
            
            with Vertical(id="result-area"):
                yield Label("Results", id="result-title")
                yield Static("Enter connection details and press Check Connection", id="result-content", classes="info")
        
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "check-button":
            self.check_connection()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.check_connection()

    def check_connection(self) -> None:
        host = self.query_one("#host-input").value
        port = self.query_one("#port-input").value
        timeout_str = self.query_one("#timeout-input").value
        result_display = self.query_one("#result-content")
        
        if not host:
            result_display.update("ERROR: Please enter a hostname or IP address")
            result_display.set_classes(["error"])
            return
        
        if not port:
            result_display.update("ERROR: Please enter a port number")
            result_display.set_classes(["error"])
            return
        
        try:
            timeout = float(timeout_str) if timeout_str else 3.0
        except ValueError:
            result_display.update(f"ERROR: Invalid timeout value: {timeout_str}. Please enter a valid number.")
            result_display.set_classes(["error"])
            return
        
        try:
            port_num = validate_port(port)
        except ValueError as e:
            result_display.update(f"ERROR: {str(e)}")
            result_display.set_classes(["error"])
            return
        
        result_display.update(f"Checking {host}:{port_num} (timeout: {timeout}s)...")
        result_display.set_classes(["info"])
        
        check_result = check_port(host, port_num, timeout)
        
        if isinstance(check_result, tuple):
            _, error_msg = check_result
            result_display.update(f"CLOSED: Port {port_num} on {host} is closed\nReason: {error_msg}")
            result_display.set_classes(["error"])
        elif check_result:
            result_display.update(f"OPEN: Port {port_num} on {host} is open and accepting connections")
            result_display.set_classes(["success"])
        else:
            result_display.update(f"CLOSED: Port {port_num} on {host} is closed")
            result_display.set_classes(["error"])

def main():
    app = SocketPeekApp()
    app.run()

if __name__ == "__main__":
    main()
