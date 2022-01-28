from jinja2 import Template
import matplotlib.pyplot as plt
from flask import Flask,render_template,request,redirect,url_for
import sys
import csv

app=Flask(__name__)
@app.route("/",methods=["POST","GET"])
def login():
    if request.method=="POST":
        cond=request.form.get("ID")
        value=request.form.get("id_value")
        try:
            return redirect(url_for("user",val=value,con=cond))
        except:
            return render_template("pages.html",error=1)
    else:
        return render_template("index.html")


##doubt
@app.route("/<val>/<con>")
def user(val,con):

    fields = []
    rows = []
    with open('data.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
    data=[]
    s=0
    if con=="student_id":
        for i in rows:
            if i[0]==val:
                data.append([i[0],i[1],i[2]])
                s+=int(i[2])
        if len(data)==0:
            return render_template("pages.html",error=1);

        return render_template("pages.html",head="Student Details",headings=fields,data=data,total=s,i='-s')

    elif con=="course_id":
        mark=[]
        for i in rows:
            if int(i[1])==int(val):
                mark.append(int(i[2]))
        s=sum(mark)
        l=len(mark)
        if l:
            av=s/l
        else:
            av=0
        try:
            max_marks=max(mark)
        except:
            max_marks=0

        if(l==0):
            return render_template("pages.html", error=1)

        data=[[av,max_marks]]
        headings = ['Average marks', 'Maximum marks']
        plt.hist(mark)
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('static/plot.png', dpi=300, bbox_inches='tight')
        return render_template("pages.html", head="Course Details", headings=headings, data=data, i='-c')



if __name__=="__main__":
    app.run(debug=True)


"""
x=str(input())
y=int(input())
template = Template(TEMPLATE)
if(x=='-s' and y in list(df['Student id'])):
    df=df[df['Student id'] == y]
    headings=df.columns
    data = df.values
    content = template.render(head="Student Details",headings=headings, data=data,i='-s',total=df[' Marks'].sum())
elif(x=='-c' and y in list(df[' Course id']) ):
    d = df.copy()
    d = d[d[' Course id'] == y]
    headings = ['Average marks', 'Maximum marks']
    data = [[d[' Marks'].mean(axis=0), d[' Marks'].max(axis=0)]]
    content = template.render(head="Course Details",headings=headings,data=data,i='-c')

    plt.hist(d[' Marks'])
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')
    plt.show()
else:
    content = template.render(error=1)

"""

