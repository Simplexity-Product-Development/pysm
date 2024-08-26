# Append parent directory to path so we can access the pysm module
import sys
sys.path.append(r'..')


def test():
    # Verify basic functionality remains unchanged
    import test_simple_on_off
    test_simple_on_off.test()

    import test_complex_hsm
    test_complex_hsm.test()
    
    import test_complex_hsm
    sm = test_complex_hsm.m
    sm.to_d2()

if __name__ == '__main__':
    test()