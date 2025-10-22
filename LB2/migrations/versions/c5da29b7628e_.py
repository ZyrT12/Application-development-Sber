from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5da29b7628e'
down_revision = '748c2474a6f1'
branch_labels = None
depends_on = None

def upgrade():
    # 0) если есть FK addresses.user_id -> users.id, временно убираем
    op.drop_constraint('addresses_user_id_fkey', 'addresses', type_='foreignkey')

    # 1) users.id: VARCHAR(36) -> UUID
    op.alter_column(
        'users', 'id',
        existing_type=sa.VARCHAR(length=36),
        type_=postgresql.UUID(),
        postgresql_using='id::uuid'
    )

    # 2) addresses.id: VARCHAR(36) -> UUID
    op.alter_column(
        'addresses', 'id',
        existing_type=sa.VARCHAR(length=36),
        type_=postgresql.UUID(),
        postgresql_using='id::uuid'
    )

    # 3) addresses.user_id: VARCHAR(36) -> UUID
    op.alter_column(
        'addresses', 'user_id',
        existing_type=sa.VARCHAR(length=36),
        type_=postgresql.UUID(),
        postgresql_using='user_id::uuid'
    )

    # 4) вернуть FK addresses.user_id -> users.id
    op.create_foreign_key(
        'addresses_user_id_fkey',
        'addresses', 'users',
        ['user_id'], ['id'],
        ondelete=None
    )

    # 5) users.description
    op.add_column('users', sa.Column('description', sa.String(), nullable=True))

    # 6) products
    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False, unique=True),
        sa.Column('price_cents', sa.Integer(), nullable=False),
    )

    # 7) orders (всё уже UUID и FK применимы)
    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('address_id', postgresql.UUID(), nullable=False),
        sa.Column('product_id', postgresql.UUID(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['address_id'], ['addresses.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
    )

def downgrade():
    # удаляем orders/products и описание, потом возвращаем типы и FK назад
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_column('users', 'description')

    op.drop_constraint('addresses_user_id_fkey', 'addresses', type_='foreignkey')

    op.alter_column('addresses', 'user_id',
        existing_type=postgresql.UUID(),
        type_=sa.VARCHAR(length=36),
        postgresql_using='user_id::text'
    )
    op.alter_column('addresses', 'id',
        existing_type=postgresql.UUID(),
        type_=sa.VARCHAR(length=36),
        postgresql_using='id::text'
    )
    op.alter_column('users', 'id',
        existing_type=postgresql.UUID(),
        type_=sa.VARCHAR(length=36),
        postgresql_using='id::text'
    )

    op.create_foreign_key(
        'addresses_user_id_fkey',
        'addresses', 'users',
        ['user_id'], ['id']
    )
