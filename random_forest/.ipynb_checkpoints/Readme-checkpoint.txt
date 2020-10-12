mat_pred[i, j, T]: 3 dimension matrix, where:
    i = # fold (starting in 0)
    j = # tree in bootstrap (from 0 to n_tree-1)
    T = maximum number of elements for test

        Let 57 rows, if #folds=6 -> T = 10 (the split would be: 10, 10, 10, 10, 10, 7)    (case 1)
        Let 63 rows, if #folds=6 -> T = 13 (the split would be: 10, 10, 10, 10, 10, 13)   (case 2)
 

mat_real[i, j]: 2 dimension matrix, where:
    i = # fold (starting in 0)
    j = test


Example for "case 1", assuming:
target:
1        ->fold1
1        ->fold1
2        ->fold1
1        ->fold2
2        ->fold2
3        ->fold2
1        ->fold3
1        ->fold3
1        ->fold3
1        ->fold4
1        ->fold4

# folds = 4 -> T = 3 

mat_real = 
1 1 2
1 2 3
1 1 1
1 1 -1

The last fold has only two cases. -1 In the last indicate that there is no test at that position


Example for "case 2", assuming:
target:
1        ->fold1
1        ->fold1
2        ->fold1
1        ->fold2
2        ->fold2
3        ->fold2
1        ->fold3
1        ->fold3
1        ->fold3
1        ->fold4
2        ->fold4
1        ->fold4
3        ->fold4
# folds = 4 -> T = 4

mat_real = 
1 1 2 -1
1 2 3 -1
1 1 1 -1
1 2 1 3

There are 3 test by fold (-1 indicates that there is element test), just in the last one have the four elements.