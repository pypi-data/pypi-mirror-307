from hello_world_rs import HelloWorld as RustHelloWorld

class HelloWorld:
    """A Python wrapper for the Rust HelloWorld class"""
    
    @staticmethod
    def greet():
        """Wrapper for the Rust greet function with additional Python functionality"""
        rust_greeting = RustHelloWorld.greet()
        return f"{rust_greeting} And hello from Python too!"