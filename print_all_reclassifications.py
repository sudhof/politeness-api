
from app import db, Reclassification


def print_all_reclassifications():
    print "\n\n"
    print "-- reclassifications --"
    recs = Reclassification.query.all()
    for rec in recs:
        print "\t", rec
    print "\n\n"


if __name__ == "__main__":


    print_all_reclassifications()



