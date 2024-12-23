# r = Read
# a = Append
# w = write
# x = Create

# Read - error if it doesn't exist

# f = open("names.txt")
# print(f.read())
# print(f.read(4))

# print(f.readline())
# print(f.readline())

# for line in f:
#     print(line)

# f.close()

# f = open("names.txt", "a")
# f.write("Neil\n")
# f.close()

# f = open("names.txt")
# print(f.read())
# f.close()

# f = open("context.txt", "w")
# f.write("i delete all of the context")
# f.close()

# f = open("context.txt")
# print(f.read())
# f.close()

# try:
#     f = open("names.txt")
#     print(f.read())
# except:
#     print("the file you want to read doent's exist")
# finally:
#     f.close()


# ce bloc copy le contenu de more_names et vide le cotenue et metre dans names

# with open("more_names.txt") as f:
#     content = f.read()

# with open("names.txt", "w") as f:
#    f.write(content)


# ici on ecrit dans un fichier
import os

if not os.path.exists("E:\Mon Bureau\OneDrive\Bureau\dav.jpg"):
    f = open("E:\Mon Bureau\OneDrive\Bureau\dav.jpg", "x")
    f.close()
    
# delete a file

# avoid an error if it doesn't exist

# if os.path.exists("dave.txt"):
#     os.remove("dave.txt")
# else:
#     print("the file you wish to delete doens't exist")
