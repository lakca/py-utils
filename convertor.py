from re import search


def try_real(s: str):
    '''Cast a real number(int and float) string to number, otherwise return directly.
    @test
    ```
    # Preserve original value
    a = 1000; assert try_real(a) is a
    a = 'a s'; assert try_real(a) is a
    # Cast
    assert try_real('1.1') == 1.1
    assert try_real('1.') == 1.0
    assert try_real('.1') == 0.1
    assert try_real('.') == '.'
    assert try_real('1') == 1
    ```
    '''
    if s == '' or s == '.':
        return s
    r = search(r'^\d*(\.?)\d*$', s)
    return s if not r else float(s) if r.group(1) else int(s)
