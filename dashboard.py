"""Final integration point - displays the results produced by calculator.py."""

from calculator import total, subtraction, multiplication, div

# --- Release banner --------------------------------------------------------
# The line below mirrors the single meaningful line of release_banner.txt.
# It is the deliberate merge-conflict target for Task 2. The wording below is
# the hand-written resolution: "fast, focused" comes from feature-banner-blue
# and "fully tested ... you can trust" comes from feature-banner-green.
RELEASE_BANNER = "Calculator Suite v1.0 - Blue/Green Edition: fast, focused and fully tested arithmetic you can trust every day"

print("*************** DASHBOARD ***************")
print(RELEASE_BANNER)
print("Result of addition is       : ", total)
print("Result of subtraction is    : ", subtraction)
print("Result of multiplication is : ", multiplication)
print("Result of division is       : ", div)
print("*****************************************")
