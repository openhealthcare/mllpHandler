"""empty message

Revision ID: 3dc621b3e1a6
Revises: 
Create Date: 2016-03-14 16:58:33.313359

"""

# revision identifiers, used by Alembic.
revision = '3dc621b3e1a6'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('error',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('glossolaliareference',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('allergy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('allergy_type', sa.String(length=250), nullable=True),
    sa.Column('allergy_type_description', sa.String(length=250), nullable=True),
    sa.Column('certainty_id', sa.String(length=250), nullable=True),
    sa.Column('certainty_description', sa.String(length=250), nullable=True),
    sa.Column('allergy_reference_name', sa.String(length=250), nullable=True),
    sa.Column('allergy_description', sa.String(length=250), nullable=True),
    sa.Column('allergen_reference_system', sa.String(length=250), nullable=True),
    sa.Column('allergen_reference', sa.String(length=250), nullable=True),
    sa.Column('status_id', sa.String(length=250), nullable=True),
    sa.Column('status_description', sa.String(length=250), nullable=True),
    sa.Column('diagnosis_datetime', sa.DateTime(), nullable=True),
    sa.Column('allergy_start_datetime', sa.DateTime(), nullable=True),
    sa.Column('no_allergies', sa.Boolean(), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatientepisode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('datetime_of_admission', sa.DateTime(), nullable=False),
    sa.Column('datetime_of_discharge', sa.DateTime(), nullable=True),
    sa.Column('visit_number', sa.String(length=250), nullable=False),
    sa.Column('admission_diagnosis', sa.String(length=250), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('merge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('old_reference_id', sa.Integer(), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.ForeignKeyConstraint(['old_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('surname', sa.String(length=250), nullable=False),
    sa.Column('first_name', sa.String(length=250), nullable=False),
    sa.Column('middle_name', sa.String(length=250), nullable=True),
    sa.Column('title', sa.String(length=250), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('birth_place', sa.String(length=250), nullable=True),
    sa.Column('sex', sa.String(length=250), nullable=True),
    sa.Column('marital_status', sa.String(length=250), nullable=True),
    sa.Column('religion', sa.String(length=250), nullable=True),
    sa.Column('date_of_death', sa.Date(), nullable=True),
    sa.Column('post_code', sa.String(length=20), nullable=True),
    sa.Column('gp_practice_code', sa.String(length=20), nullable=True),
    sa.Column('ethnicity', sa.String(length=250), nullable=True),
    sa.Column('death_indicator', sa.Boolean(), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patientidentifier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('identifier', sa.String(length=250), nullable=True),
    sa.Column('issuing_source', sa.String(length=250), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('lab_number', sa.String(length=250), nullable=True),
    sa.Column('profile_code', sa.String(length=250), nullable=True),
    sa.Column('request_datetime', sa.DateTime(), nullable=True),
    sa.Column('observation_datetime', sa.DateTime(), nullable=True),
    sa.Column('last_edited', sa.DateTime(), nullable=True),
    sa.Column('result_status', sa.String(length=250), nullable=True),
    sa.Column('observations', sa.Text(), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('system', sa.String(length=250), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('gloss_reference_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gloss_reference_id'], ['glossolaliareference.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inpatientlocation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('inpatient_episode_id', sa.Integer(), nullable=True),
    sa.Column('datetime_of_transfer', sa.DateTime(), nullable=True),
    sa.Column('ward_code', sa.String(length=250), nullable=True),
    sa.Column('room_code', sa.String(length=250), nullable=True),
    sa.Column('bed_code', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['inpatient_episode_id'], ['inpatientepisode.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('inpatientlocation')
    op.drop_table('subscription')
    op.drop_table('result')
    op.drop_table('patientidentifier')
    op.drop_table('patient')
    op.drop_table('merge')
    op.drop_table('inpatientepisode')
    op.drop_table('allergy')
    op.drop_table('glossolaliareference')
    op.drop_table('error')
    ### end Alembic commands ###