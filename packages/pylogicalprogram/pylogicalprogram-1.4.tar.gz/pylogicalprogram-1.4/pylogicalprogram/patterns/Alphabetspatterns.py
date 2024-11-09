
size = 7
class AlphabetLetterPrint():
    def print_a(self):
        end = size * 2 - 1
        a_line = []
        for i in range(size):
            line = ""
            for j in range(end):
                if j == size - i - 1 or j == size + i - 1 or (i == size // 2 and j > size - i - 1 and j < size + i):
                    line += "*"
                else:
                    line += " "
            a_line.append(line)
        return a_line
    def print_b(self):
        start = 1
        end = size + 1
        middle = end // 2
        b_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j == start or (i == start and j < size) or (i == middle and j < size) or \
                        (i == size and j < size) or (j == size and (i < middle and i != start)) or \
                        (j == size and (i > middle and i != size)):
                    line += "* "
                else:
                    line += "  "
            b_line.append(line)
        return b_line

    def print_c(self):
        start = 1
        end = size + 1
        c_lines = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i == size and start < j and j < size) or (i == start and start < j and j < size) or (j == start and start < i and i < size):
                    line += "* "
                else:
                    line += "  "
            c_lines.append(line)
        return c_lines

    def print_d(self):
        start = 1
        end = size + 1
        d_lines = []
        for row in range(start, end):
            line = ""
            for col in range(start, end):
                if col == start or (col == size and row != start and row != size) or (row == start or row == size) and col < size:
                    line += "* "
                else:
                    line += "  "
            d_lines.append(line)
        return d_lines

    def print_e(self):
        start = 1
        end = size + 1
        middle = end // 2
        e_lines = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or i == size or (i==middle and j<=middle) or j==1:
                    line += "* "
                else:
                    line += "  "
            e_lines.append(line)
        return e_lines

    def print_f(self):
        start = 1
        end = size + 1
        middle = end // 2
        f_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i==start or j==start or (i==middle and j<=middle):
                    line += "* "
                else:
                    line += "  "
            f_line.append(line)
        return f_line

    def print_g(self):
        start = 1
        end = size + 1
        middle = end // 2
        g_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i==start or i==size or j==start or (i==middle and middle<=j) or (j==size and middle<=i):
                    line += "* "
                else:
                    line += "  "
            g_line.append(line)
        return g_line

    def print_h(self):
        start = 1
        end = size + 1
        middle = end // 2
        h_lines = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j == start or j == size or i == middle:
                    line += "* "
                else:
                    line += "  "
            h_lines.append(line)
        return h_lines

    def print_i(self):
        start = 1
        end = size + 1
        middle = end // 2
        i_lines = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or i == size or j == middle:
                    line += "* "
                else:
                    line += "  "
            i_lines.append(line)
        return i_lines

    def print_j(self):
        start = 1
        end = size + 1
        middle = end // 2
        g_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or j==middle or (i==size and middle>=j) or (j==start and middle<=i):
                    line += "* "
                else:
                    line += "  "
            g_line.append(line)
        return g_line

    def print_k(self):
        start = 1
        end = size + 1
        middle = end //2
        k_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j==middle-1 or (j == size+1-i and i<=middle) or (i > middle and j == i):
                    line += "* "
                else:
                    line += " "
            k_line.append(line)
        return k_line

    def print_l(self):
        start = 1
        end = size + 1
        l_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j==start or i==size:
                    line += "* "
                else:
                    line += "  "
            l_line.append(line)
        return l_line

    def print_m(self):
        start = 1
        end = size + 1
        middle = end // 2
        m_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j == start or j == size or (i == j and i <= middle) or (j == size - i + 1 and i <= middle):
                    line += "* "
                else:
                    line += "  "
            m_line.append(line)
        return m_line

    def print_n(self):
        start = 1
        end = size + 1
        n_lines = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j == start or j == size or i==j:
                    line += "* "
                else:
                    line += "  "
            n_lines.append(line)
        return n_lines

    def print_o(self):
        start = 1
        end = size + 1
        o_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i==size and start<j and j<size) or (i==start and start<j and j<size) or (j==start and start<i and i<size) or (j==size and start<i and size>i):
                    line += "* "
                else:
                    line += "  "
            o_line.append(line)
        return o_line

    def print_p(self):
        start = 1
        end = size + 1
        middle = end // 2
        p_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j == start or i == start or (i == middle and j < end) or (j == size and i < middle):
                    line += "* "
                else:
                    line += "  "
            p_line.append(line)
        return p_line

    def print_q(self):
        start = 1
        end = size + 1
        middle = end // 2
        q_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i==size and start<j and j<size) or (i==start and start<j and j<size) or (j==start and start<i and i<size) or (j==size and start<i and size>i)\
                        or (i==j and middle<=j):
                    line += "* "
                else:
                    line += "  "
            q_line.append(line)
        return q_line

    def print_r(self):
        start = 1
        end = size + 1
        middle = end // 2
        r_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (j == start or i == start or (j == size and i <= middle) or (i == middle and j <= size) or (i > middle and j == i)):
                    line += "* "
                else:
                    line += "  "
            r_line.append(line)
        return r_line

    def print_s(self):
        s_line = []

        for i in range(size):
            line = ""
            for j in range(size):
                if (i == 0 and j > 0) or (i == size - 1 and j < size - 1) or (i == size // 2) or \
                        (j == 0 and i < size // 2 and i != 0) or (j == size - 1 and i > size // 2 and i != size - 1):
                    line += "* "
                else:
                    line += "  "
            s_line.append(line)
        return s_line

    def print_t(self):
        start = 1
        end = size + 1
        middle = end // 2
        t_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i==start or j==middle:
                    line += "* "
                else:
                    line += "  "
            t_line.append(line)
        return t_line

    def print_u(self):
        start = 1
        end = size + 1
        middle = end // 2
        u_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (j==start and i<size) or (j==size and i<size) or (i==size and start<j and j<size):
                    line += "* "
                else:
                    line += "  "
            u_line.append(line)
        return u_line

    def print_v(self):
        start = 1
        end = size + 1
        v_line = []
        for i in range(start, end):
            line = ""
            for j in range(2 * end - 1):
                if j == i or j == (2 * end - 2 - i):
                    line += "*"
                else:
                    line += " "
            v_line.append(line)
        return v_line

    def print_w(self):
        start = 1
        end = size + 1
        middle = end // 2
        w_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if j == start or j == size or (i == j and i >= middle) or (j == size - i + 1 and i >= middle):
                    line += "* "
                else:
                    line += "  "
            w_line.append(line)
        return w_line

    def print_x(self):
        start = 1
        end = size + 1
        x_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i==j or i+j==end:
                    line += "* "
                else:
                    line += "  "
            x_line.append(line)
        return x_line

    def print_y(self):
        start = 1
        end = size + 1
        middle = end //2
        y_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (j == i and i<=middle)  or (j == end-i and i<middle) or (j==middle and middle<=i):
                    line += "* "
                else:
                    line += "  "
            y_line.append(line)
        return y_line

    def print_z(self):
        start = 1
        end = size + 1
        z_line = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i==start or i==size or i+j==end:
                    line += "* "
                else:
                    line += "  "
            z_line.append(line)
        return z_line

printer = AlphabetLetterPrint()

def print_name(name):
    name = name.lower()
    name_lines = [""] * size
    for letter in name:
        method = getattr(printer, f"print_{letter}", None)
        if method:
            letter_lines = method()
            for i in range(size):
                name_lines[i] += letter_lines[i] + " "
    return "\n".join(name_lines)
