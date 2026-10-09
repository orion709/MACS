from textual.app import App, ComposeResult
from textual.wigets import Footer, Header

class MACS(app):

    BINDINGS = []
    
    def compose(self) -> ComposeResult:
        yield Header
        yield Footer

if __name__ == "__main__":
    MACS.run()