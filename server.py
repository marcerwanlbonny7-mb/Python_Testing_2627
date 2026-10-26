import json
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect, flash, url_for, session
)


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def isUpcoming(competition):
    compDate = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    return compDate >= datetime.now()


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
bookings = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    found = [club for club in clubs if club['email'] == email]
    if not found:
        flash("Unknown email, please try again")
        return redirect(url_for('index'))
    club = found[0]
    session['club'] = club['name']
    upcoming = [c for c in competitions if isUpcoming(c)]
    return render_template(
        'welcome.html', club=club, competitions=upcoming
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if session.get('club') != club:
        if session.get('club'):
            flash("You can only make bookings for your own club")
        else:
            flash("Please log in first")
        return redirect(url_for('index'))
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [
        c for c in competitions if c['name'] == competition
    ]
    if not foundClub or not foundCompetition:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))
    if not isUpcoming(foundCompetition[0]):
        flash("This competition has already taken place")
        return redirect(url_for('index'))
    return render_template(
        'booking.html', club=foundClub[0], competition=foundCompetition[0]
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    if not session.get('club'):
        flash("Please log in first")
        return redirect(url_for('index'))
    if request.form.get('club') != session.get('club'):
        flash("You can only make bookings for your own club")
        return redirect(url_for('index'))
    foundCompetition = [
        c for c in competitions
        if c['name'] == request.form['competition']
    ]
    foundClub = [c for c in clubs if c['name'] == request.form['club']]
    if not foundCompetition or not foundClub:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))
    competition = foundCompetition[0]
    club = foundClub[0]
    if not isUpcoming(competition):
        flash("This competition has already taken place")
        return redirect(url_for('index'))
    bookingUrl = url_for(
        'book', competition=competition['name'], club=club['name']
    )
    try:
        placesRequired = int(request.form['places'])
    except (ValueError, TypeError):
        flash("Invalid number of places")
        return redirect(bookingUrl)
    if placesRequired < 1:
        flash("Invalid number of places")
        return redirect(bookingUrl)
    if placesRequired > 12:
        flash("Cannot book more than 12 places")
        return redirect(bookingUrl)
    bookedKey = (club['name'], competition['name'])
    alreadyBooked = bookings.get(bookedKey, 0)
    if alreadyBooked + placesRequired > 12:
        flash("Cannot book more than 12 places")
        return redirect(bookingUrl)
    if int(competition['numberOfPlaces']) == 0:
        flash("This competition is full")
        return redirect(bookingUrl)
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Not enough places available")
        return redirect(bookingUrl)
    if placesRequired > int(club['points']):
        flash("Not enough points")
        return redirect(bookingUrl)
    competition['numberOfPlaces'] = (
        int(competition['numberOfPlaces']) - placesRequired
    )
    club['points'] = int(club['points']) - placesRequired
    bookings[bookedKey] = alreadyBooked + placesRequired
    flash(f'Great-booking complete! {placesRequired} places booked.')
    return render_template(
        'welcome.html', club=club, competitions=competitions
    )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
