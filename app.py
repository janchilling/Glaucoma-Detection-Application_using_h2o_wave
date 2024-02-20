from h2o_wave import main, app, Q, ui, on, run_on
from prediction_system.prediction_function import predictor
import uuid 
import os

@app('/')
async def serve(q: Q):
    if not q.client.initialized:
        await init(q)
        q.client.initialized = True

    await run_on(q)
    await q.page.save()

async def init(q: Q) -> None:
    q.client.cards = set()
    q.client.dark_mode = False

    q.page['header'] = ui.header_card(
        box='2 1 8 1',
        title='Glaucoma Detection Application',
        subtitle="The assignment for the H2O Wave internship",
        image='https://wave.h2o.ai/img/h2o-logo.svg'
    )

    q.page['meta'] = ui.meta_card(
        box='',
        title='Glaucoma Detection',
        theme='light',
    )

    q.page['instructions'] = ui.form_card(
        box='4 2 3 1', 
        items=[ui.text_l(
            "Upload a Retinal Image of the eye for detection"
        )]
    )

    q.page["userInput"] = ui.form_card(
        box="2 3 4 3",  # Adjusted to fit side by side
        items=[
            ui.file_upload(
                name='file_upload', 
                label='Detect'
            )
        ],
    )

    q.page['prediction'] = ui.article_card(
        box='6 3 4 3',  # Adjusted to fit side by side
        title='Result',
        content=f'The results will be shown here.'
    )
    
    q.page['footer'] = ui.footer_card(
        box='1 8 -1 1',
        caption='This Glaucoma Detection application was made with 💛 using [H2O Wave](https://wave.h2o.ai).'
    )

    await home(q)

UPLOAD_DIR = 'uploads'

@on('file_upload')
async def detect_Glaucoma(q: Q):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    upload_files = q.args['file_upload']
    upload_file = upload_files[0]  # Access the first uploaded file

    # Generate a unique file name
    file_name = str(uuid.uuid4()) + '.jpg'

    # Save the uploaded file to the uploads directory
    file_path = os.path.join(UPLOAD_DIR, file_name)
    file = await q.site.download(upload_file, file_path)

    q.page['image'] = ui.form_card(
        box='4 6 4 4', 
        items=[
            ui.image(
                'Image Stream', 
                path=file_path
                )])
    
    q.page['footer'] = ui.footer_card(
        box='1 10 -1 1',
        caption='This Glaucoma Detection application was made with 💛 using [H2O Wave](https://wave.h2o.ai).'
    )

    # Use the downloaded file path for prediction
    prediction = await predictor.predict(file_path)
    q.page['prediction'].content = f'Prediction: {prediction}'
    await q.page.save()

@on()
async def home(q: Q):
    clear_cards(q)
    add_card(q, 'form', ui.form_card(box='vertical', items=[ui.text('This is my app!')]))

def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

def clear_cards(q, ignore=[]) -> None:
    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)
