from flask import Flask, render_template, request, redirect, send_file
from so_scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
  return render_template("job.html")

@app.route("/report")
def report():
  searchword = request.args.get('searchword')
  if searchword:  
    searchword = searchword.lower() 
    fromDB = db.get(searchword)
    if fromDB:
      jobs = fromDB
    else:
      jobs = get_jobs(searchword)
      db[searchword] = jobs
  else:
    return redirect("/") 
  return render_template("report.html", searchword = searchword, resultsNumber=len(jobs), jobs = jobs)

@app.route("/export")
def export():
  try:
    searchword = request.args.get('searchword')
    if not searchword:  #검색어없으면 예외로
      raise Exception()
    searchword = searchword.lower() 
    fromDB = db.get(searchword)
    if not fromDB: #데이터베이스에 없으면 예외로
      raise Exception()
    save_to_file(fromDB) 
    return send_file("downloadjobs.csv")
  except: #예외로 오면 밑에 코드 처리
    return redirect("/")


app.run(host="0.0.0.0")