import midtransclient

# Konfigurasi Midtrans
MIDTRANS_SERVER_KEY = 'SB-Mid-server-NABuRaMuXUZ0TUoKyOUzNjID'
MIDTRANS_CLIENT_KEY = 'SB-Mid-client-ryYGvj4AW44b_DhE'

def get_snap_client():
    snap = midtransclient.Snap(
        is_production=False,  # Set True jika menggunakan environment production
        server_key=MIDTRANS_SERVER_KEY
    )
    return snap
