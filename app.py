from h2o_wave import main, app, Q, ui, on, run_on
from prediction_system.prediction_function import predictor
import os
import uuid
from utils import add_card, clear_cards

UPLOAD_DIR = 'uploads'

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
        subtitle="The assignment for the H2O.ai internship",
        image='https://wave.h2o.ai/img/h2o-logo.svg',
        items=[
            ui.link(
                name="github_btn",
                path="https://github.com/janchilling/Glaucoma-Detection-Application_using_h2o_wave.git",
                label="GitHub",
                button=True,
            )
        ],
    )

    q.page['meta'] = ui.meta_card(
        box='',
        title='Glaucoma Detection',
        theme='light',
    )

    q.page['instructions'] = ui.article_card(
        box='4 5 4 2',
        title="Instructions",
        content='''
1. Get a Retinal image of your eye with a suitable device.
2. Drag or Browse the image and enter to the Input column.
3. Click Detect.
4. Check the Results column for the result.
'''
    )

    q.page["userInput"] = ui.form_card(
        box="2 2 4 3",
        items=[
            ui.file_upload(
                name='file_upload',
                label='Detect'
            )
        ],
    )

    q.page['prediction'] = ui.article_card(
        box='6 2 4 3',
        title='Result',
        content=f'The result will be shown here.'
    )

    q.page['footer'] = ui.footer_card(
        box='1 8 -1 1',
        caption='This Glaucoma Detection application was made with 💛 using [H2O Wave](https://wave.h2o.ai).'
    )

    await home(q)

# Handling the image upload and the prediction
@on('file_upload')
async def detect_Glaucoma(q: Q):

    # Creating an uploads folder to store the images, only if uploads folder already doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Getting the temporary image path in the server
    upload_files = q.args['file_upload']
    upload_file = upload_files[0]

    # Creating an unique filename for the uploaded image
    file_name = str(uuid.uuid4()) + '.jpg'

    # Sending the file to the uploads directory
    file_path = os.path.join(UPLOAD_DIR, file_name)
    await q.site.download(upload_file, file_path)

    # Removing the instructions compoenent
    del q.page['instructions']

    # Showing the user uploaded image and adjusting the footer
    q.page['image'] = ui.image_card(
        box='4 5 4 4',
        title='Provided Retinal image',
        path=upload_file
    )

    q.page['footer'] = ui.footer_card(
        box='1 9 -1 1',
        caption='This Glaucoma Detection application was made with 💛 using [H2O Wave](https://wave.h2o.ai).'
    )

    # Passing the file path to the predictor function and updating the result
    prediction = await predictor.predict(file_path)
    q.page['prediction'].content = f'{prediction}'
    await q.page.save()

@on()
async def home(q: Q):
    clear_cards(q)
    add_card(q, 'form', ui.form_card(box='vertical', items=[ui.text('This is my app!')]))
