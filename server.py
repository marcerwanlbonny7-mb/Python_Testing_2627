import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


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
    return render_template(
        'welcome.html', club=club, competitions=competitions
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club]
    foundCompetition = [
        c for c in competitions if c['name'] == competition
    ]
    if not foundClub or not foundCompetition:
        flash("Something went wrong-please try again")
        return redirect(url_for('index'))
    return render_template(
        'booking.html', club=foundClub[0], competition=foundCompetition[0]
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
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
    return redirect(url_for('index'))
