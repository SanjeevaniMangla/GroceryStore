from application import db


class ProductCategoryAssociation(db.Model):
    __tablename__ = 'product_category_association'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)