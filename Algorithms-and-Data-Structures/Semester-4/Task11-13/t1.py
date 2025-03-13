# 4.3. Псевдокод разработанного алгоритма
# Sk - независимое множество вершин ,
# покрашенных в цвет k.
# begin
# 1. k := 1;
# 2. for i=0 to n
# 3. if i ∉ V then continue
# /*vertex i is coloured*/
# 4. Sk := Sk ⋃ {i};
# 5. V := V\{i};
# 6. while i has not coloured nonneighbours /* row i contains 0*/
# 7. for j=i+1 to n-1
# /* find the first non- neighbor*/
# 8. if aij = 0 AND j ∈ V
# then break
# 9. end for
# 10. if j = n then break
# 11. Sk := Sk ⋃ {j};
# 12. V := V\{j};
# 13. Ai
# := Ai ˅ Aj
# ;
# 14. end while
# 15. k := k+1;
# 16. end for
# end
#
# https://publications.hse.ru/pubs/share/folder/0rhqzr8ukk/133671897.pdf