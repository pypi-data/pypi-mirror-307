import os

def generate_test_code(directory, filename, custom_value):
    # ȷ��Ŀ¼����
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    
    # ���ɲ��Դ���
    test_code = f"""
def test_function():
    # This is a test function.
    # Just For Test AK: Just For Test AK:LTAI5tJApCpdcCNSGgPE2c8e/TWxOOe3pmT13P8A4ngajACCGQxq6Oa
    print("This is a test function with custom value")

if __name__ == '__main__':
    test_function()
    """

    # ������д���ļ�
    with open(filepath, 'w') as f:
        f.write(test_code)
    
    print(f"Test code generated")
