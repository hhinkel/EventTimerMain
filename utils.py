import datetime
from setup import Setup

class Utils:

    def division_setup(self, db, setup):
        #database must be open, connected and a cursor defined.
        setup = Setup('setup.json')
        for division in setup.divisions:
            optTime = self.determine_time(division[1], division[4])
            minTime = self.determine_time(division[2], division[4])
            db.dbCursor.execute("INSERT INTO xcDivisionTable VALUES (?,?,?,?,?,?,?,?,?)",
                                (division[0], int(division[1]), int(division[2]), int(division[3]), int(division[4]),
                                 optTime, minTime, int(division[5]), int(division[6])))
            db.dbConnection.commit()

    def determine_time(self, mpermin, distance):
        # formula from http://www.myhorsechat.com/2013/03/14/how-to-calculate-the-optimum-time-in-eventing/
        # convert meters per min to meters per second
        mpersec = int(mpermin) / 60

        # determine the number of seconds needed to cover the distance at the meters per second determined above
        totalsecs = int(distance) / mpersec

        return str(datetime.timedelta(seconds=totalsecs))
