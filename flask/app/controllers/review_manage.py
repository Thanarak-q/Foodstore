from flask import (jsonify, render_template,
                  request, url_for, flash, redirect)

from app import app
from app import db
from app.models.review import Review
from flask_login import login_required, current_user

@app.route('/reviews/get_all_reviews')
def reviews_list():
    db_allreview = Review.query.all()
    reviews = list(map(lambda x: x.to_dict(), db_allreview))
    reviews.sort(key=(lambda x: int(x['review_id'])))
    return jsonify({"reviews": reviews})

@app.route('/reviews/create', methods=('GET', 'POST'))
def review_create():
    
    if request.method == 'POST':
        app.logger.debug("review - CREATE")
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['name', 'star', 'review']
        validated = True
        validated_dict = dict()
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break

            validated_dict[key] = value
        app.logger.debug(validated_dict)
        if validated:
            try:
                temp = Review(
                    name=validated_dict['name'],
                    star=validated_dict['star'],
                    review=validated_dict['review']
                )
                db.session.add(temp)
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new review: {ex}")
                raise
            
    return reviews_list()

@app.route('/reviews/update', methods=('GET', 'POST'))
@login_required
def review_update():
    
    if request.method == 'POST':
        if current_user.role != 'Admin':
            return 'You are not Admin'
        
        app.logger.debug("review - UPDATE")
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['review_id', 'name', 'star', 'review']
        validated = True
        validated_dict = dict() 
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break

            validated_dict[key] = value
        app.logger.debug(validated_dict)
        if validated:
            try:
                review = Review.query.get(validated_dict['review_id'])
                review.update(name=validated_dict['name'],
                              review=validated_dict['review'],
                              star=validated_dict['star'])
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new review: {ex}")
                raise
            
    return reviews_list()

@app.route('/reviews/delete', methods=('GET', 'POST'))
@login_required
def review_delete():
    
    if request.method == 'POST':
        if current_user.role != 'Admin':
            return 'You are not Admin'
        
        app.logger.debug("review - DELETE")
        result = request.form.to_dict()
        app.logger.debug(result)
        valid_keys = ['review_id']
        validated = True
        validated_dict = dict() 
        for key in result:
            app.logger.debug(f"{key}: {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break

            validated_dict[key] = value
        app.logger.debug(validated_dict)
        if validated:
            try:
                review = Review.query.get(validated_dict['review_id'])
                db.session.delete(review)
                
                db.session.commit()
                
            except Exception as ex:
                app.logger.error(f"Error create new review: {ex}")
                raise
            
    return reviews_list()