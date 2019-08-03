from flask import Blueprint, render_template

mod = Blueprint('home', __name__)

class HomeController():
  @mod.route('/')
  def get():
    return render_template('home/show.html')
