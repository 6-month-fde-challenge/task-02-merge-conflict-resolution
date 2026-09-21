"""Final integration point - displays the results produced by calculator.py."""

from calculator import total, subtraction, multiplication, div

# --- Release banner --------------------------------------------------------
# The line below mirrors the single meaningful line of release_banner.txt.
# It is the deliberate merge-conflict target for Task 2.
RELEASE_BANNER = "Calculator Suite v1.0 - release banner pending final wording"

print("*************** DASHBOARD ***************")
print(RELEASE_BANNER)
print("Result of addition is       : ", total)
print("Result of subtraction is    : ", subtraction)
print("Result of multiplication is : ", multiplication)
print("Result of division is       : ", div)
print("*****************************************")
