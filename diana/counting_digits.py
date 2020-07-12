# def count_digits(n):
#     tot = 0
#     for i in range(1, n+1):
#         while i != 0:
#             tot += 1
#             i //= 10
#     return tot
#
# print(count_digits(2040))


# t = "Hello, World!"
#
# lst = []
# for chr in t:
#     if chr.isalpha():
#         lst.append(chr)
# print(lst)
#
# print([chr for chr in t if chr.isalpha()])
#
#
# class Converter:
#     def get_miles_to_km_factor(self):
#         return 1.6
#     def miles_to_km(self, miles):
#         return self.get_miles_to_km_factor() * miles
#
# class NautConverter:
#     def get_miles_to_km_factor(self):
#         return 1.8
#
# converter = NautConverter()
# print(converter.miles_to_km(15))

import re


def change_date_format(dates):
    res = []
    for date in dates:
        d0 = re.match(r'([0-9]{4})/([0-9]{2})/([0-9]{2})', date)
        d1 = re.match(r'([0-9]{2})/([0-9]{2})/([0-9]{4})', date)
        d2 = re.match(r'([0-9]{2})-([0-9]{2})-([0-9]{4})', date)
        d3 = re.match(r'([0-9]{4})([0-9]{2})([0-9]{4})', date)
        print(d0, d1, d2, d3)
        if d0:
            d = d0.group(0)+d0.group(1)+d0.group(2)
        elif d1:
            d = d1.group(0) + d1.group(1) + d1.group(2)
        elif d2:
            d = d2.group(0) + d2.group(1) + d2.group(2)
        elif d3:
            d = d3.group(0) + d3.group(1) + d3.group(2)
        else:
            d = None
        if d is not None:
            res.append(d)
    return res


if __name__ == "__main__":
    dates = change_date_format(["2010/03/30", "15/12/2016", "11-15-2012", "20130720"])
    print(*dates, sep='\n')