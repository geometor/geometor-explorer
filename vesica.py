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
    # TODO: add label to Models
    A = M.set_point(0, 0)
    B = M.set_point(1, 0)
    l1 = M.construct_line(A, B)

    c1 = M.construct_circle(A, B)
    C = M.points()[-1]

    c2 = M.construct_circle(B, A)
    D = M.points()[-3]
    E = M.points()[-2]
    F = M.points()[-1]

    t1 = M.set_polygon([A, B, E])
    t2 = M.set_polygon([A, B, F])

    #  l2 = M.gen_line(E, F)
    #  c2 = M.gen_circle(A, D)
    #  c3 = M.gen_circle(B, C)

    print(M)
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
