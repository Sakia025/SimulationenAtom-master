

outputfile = 'Ergebnisse/TDK-Werte'
with open(outputfile, 'wt') as out_file:
    out_file.write('z/mm \t Dosis/Gy \t Dosis error/Gy \t Dosis_error/%\n')
    for i in range(5):
        out_file.write('bla\t'.format())
