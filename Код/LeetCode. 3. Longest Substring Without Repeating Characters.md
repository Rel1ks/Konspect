````Python
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        char_index = {}  # храним последний индекс каждого символа
        left = 0         # левая граница окна
        max_length = 0   # максимальная длина
        
        for right, char in enumerate(s):
            # Если символ уже есть в текущем окне, сдвигаем левую границу
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            
            # Обновляем индекс текущего символа
            char_index[char] = right
            
            # Обновляем максимальную длину
            max_length = max(max_length, right - left + 1)
        
        return max_length
````
![[Снимок экрана от 2026-02-04 11-54-23.png]]
