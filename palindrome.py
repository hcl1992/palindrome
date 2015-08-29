from __future__ import division
import sys

def add_delim(string, char):
    """Add delimeter char to bookend and separate string chars."""
    return char + char.join(list(string.lower())) + char

def adjust_pos(left, center, right, adj_right):
    """If ctr unmoved, set to adj_right. Mirror left around ctr."""
    if (left + right) / 2 == center:
        center = adj_right
    left = center - (right - center)
    return left, center, right

def find_sps(string, delim):
    """"""
    if string == '': return [0]

    text = add_delim(string, delim)
    len_text = len(text)
    len_sps = [0] * len_text

    L, C, R = 1, 1, 1
    L_edge, R_edge = 1, len(text) - 2

    while R <= R_edge:

        # expand naively around current center; single char is palindrome
        while L >= L_edge and R <= R_edge and text[L] == text[R]:
            if text[R] != delim:
                len_sps[C] += 1 if L == R else 2
            L, R = L - 1, R + 1

        # expand as much as possible using "mirror" principle
        adj_right = R - 1 if len_sps[C] > 0 and L > 0 else R
        for i in xrange(1, R - C):
            dist_to_edge = adj_right - (C + i)

            if len_sps[C - i] < dist_to_edge:
                len_sps[C - i] = len_sps[C + i]
            elif len_sps[C - i] > dist_to_edge:
                len_sps[C + i] = dist_to_edge
            else:
                len_sps[C + i] = dist_to_edge
                C += i
                break

        # reset position indices
        L, C, R = adjust_pos(L, C, R, adj_right)

    return len_sps

def longest_sp(string, delim='|'):
    """Find longest subpalindrome (SP) within given string.
    Returns
        tuple of ints (start, end), which return the longest SP
        when used to slice string[start: end]
    """
    len_sps = find_sps(string, delim)
    longest = max(len_sps)

    # account for presence of delimeters; int takes floor of float
    ctr_ind = int(len_sps.index(longest) / 2)
    half_word = int(longest / 2)

    start, end = ctr_ind - half_word, ctr_ind + half_word
    end += 0 if longest % 2 == 0 else 1

    return start, end

# Test

def test_add_delim():
    """Test add_delim() for some corner cases."""
    assert '||' == add_delim('', '|'), 'empty case fails'
    assert '|a|' == add_delim('a', '|'), 'single char case fails'
    assert ',a,b,' == add_delim('ab', ','), 'two char case fails'
    return True

def test_adjust_pos():
    """Test various cases for adjust_pos()."""
    assert (19, 20, 21) == adjust_pos(1, 11, 21, 20)
    assert (3, 5, 7) == adjust_pos(1, 5, 7, 6)
    assert (19, 19, 19) == adjust_pos(3, 11, 19, 19)
    assert (11, 15, 19) == adjust_pos(3, 15, 19, 19)
    return True

def test_longest_sp():
    """Test longest_SP() with different inputs."""
    L = longest_sp
    assert L('babcbabcbaccba') == (1, 10)
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carrrs') == (7, 10)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8, 21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    assert L('amanaplanacanalpanama') == (0, 21)
    assert L('aabcd') == (0, 2)
    return True

def unit_tests():
    """Unit tests."""
    test_add_delim()
    test_adjust_pos()
    test_longest_sp()
    return True

# Main

def main(string):
    """Return longest palindromic substring, or subpalindrome (SP)."""
    start, end = longest_sp(string)
    pal = string[start:end]
    print pal
    return pal

if __name__ == '__main__':
    unit_tests()
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print 'Call with single argument, e.g. python palindrome.py racecar'
