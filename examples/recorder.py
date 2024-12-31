from TotoBotRec.totoBotRec import *

record(considerCursor=False, considerWait=True, waitThreshold=3000)

records = getRecords()
print(records[0])
for r in records[1:]:
    print(f"Then {str(r)}")