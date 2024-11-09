"""My Info class"""
# pylint: disable=invalid-name

class Info:
    """My Info Class"""
    @staticmethod
    def info(s, **kwargs):
        """info"""
        print(f"[I] {s}", **kwargs)
    
    @staticmethod
    def warn(s, **kwargs):
        """warn with yellow font"""
        print(f"\033[93m[W] {s}\033[0m", **kwargs)
    
    @staticmethod
    def WARN(s, **kwargs):
        """warn with yellow back"""
        print(f"\033[103m[W] {s}\033[0m", **kwargs)
    
    @staticmethod
    def error(s, **kwargs):
        """print error with red font"""
        print(f"\033[91m[E] {s}\033[0m", **kwargs)
