"""
test script for geometor package
"""
from geometor import *

if __name__ == '__main__':

    sp.init_printing()

    NAME = 'vesica'
    NAME += input(f'\nsession name: {NAME}')
    log_init(NAME)
    start_time = timer()

    print_log(f'\nMODEL: {NAME}')

    M = Model()
    A = M.set_point(0, 0, classes=['start'], label='A')
    B = M.set_point(1, 0, classes=['start'], label='B')

    l_1 = M.construct_line(A, B)

    c_1 = M.construct_circle(A, B)
    C = M.points()[-1]
    M.labels[C] = 'C'

    c_2 = M.construct_circle(B, A)
    D = M.points()[-3]
    E = M.points()[-2]
    F = M.points()[-1]
    M.labels[D] = 'D'
    M.labels[E] = 'E'
    M.labels[F] = 'F'

    t_1 = M.set_polygon([A, B, E])
    M.labels[t_1] = 't_1'
    t_2 = M.set_polygon([A, B, F])
    M.labels[t_2] = 't_2'

    l_2 = M.construct_line(E, F)
    c_3 = M.construct_circle(A, D)
    c_4 = M.construct_circle(B, C)

    M.summary()

    print_log(f'\nANALYZE: {NAME}')
    sections, sections_by_line = analyze_golden(M)


    # PLOT *********************************
    print_log(f'\nPLOT: {NAME}')

    fig, (ax, ax_btm) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [10, 1]})
    plt.tight_layout()

    plot_model(NAME, ax, ax_btm, M)

    #  title = f'G E O M E T O R'
    #  fig.suptitle(title, fontdict={'color': '#960', 'size':'small'})

    print_log('\nPlot Goldens')
    plot_sections(NAME, ax, ax_btm, sections)

    plot_all_sections(NAME, ax, ax_btm, M, sections)

    print_log('\nPlot Golden Groups')
    groups = group_sections(sections)
    plot_all_groups(NAME, ax, ax_btm, M, groups)


    #  plt.show()
