import streamlit as st
# from img_classification import teachable_machine_classification
# from PIL import Image, ImageOps
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import datetime
# import configparser
import webbrowser
import openai
from openai.error import InvalidRequestError

# authentification
with open('./bla.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    # page = st.sidebar.selectbox("探索或预测", ("苹果病分类",
    #     "葡萄病分类",
    #     "马铃薯病分类",
    #     "番茄病分类"))

    # if page == "苹果病分类":
    st.title("使用 DALL-E 生成图像")
    st.write("教程[link](https://learndataanalysis.org/source-code-use-ai-to-create-images-with-python-tutorial-for-beginners-openai-dall-e-api/)")
    def generate_image(prompt, num_image=1, size='512x512', output_format='url'):
        """
        params:
            prompt (str):
            num_image (int):
            size (str):
            output_format (str):
        """
        try:
            images = []
            response = openai.Image.create(
                prompt=prompt,
                n=num_image,
                size=size,
                response_format=output_format
            )
            if output_format == 'url':
                for image in response['data']:
                    images.append(image.url)
            elif output_format == 'b64_json':
                for image in response['data']:
                    images.append(image.b64_json)
            return {'created': datetime.datetime.fromtimestamp(response['created']), 'images': images}
        except InvalidRequestError as e:
            print(e)

    # config = configparser.ConfigParser() 
    # config.read('credential.ini')
    # API_KEY = config['openai']['APIKEY']
    openai.api_key = st.secrets["OPENAI_KEY"]

    SIZES = ('1024x1024', '512x512', '256x256')

    # generate images (url outputs)
    prompt = st.text_input("Prompt", value="这里输入...")
    sizz = st.select_slider("大小", options=(['1024x1024', '512x512', '256x256']))
    # st.write(sizz)
    if st.button("生成"):
        with st.spinner("生成图像..."):
            response = generate_image(prompt, num_image=1, size=SIZES[0])
            response['created']
            images = response['images']
            for image in images:
                webbrowser.open(image)
                st.write("教程[link]("+image+")")

            ## generate images (byte output)
            # response = generate_image('San Francisco and Chicago mixed', num_image=2, size=SIZES[1], output_format='b64_json')
            # prefix = 'demo'
            # for indx, image in enumerate(response['images']):
            #     with open(f'{prefix}_{indx}.jpg', 'wb') as f:
            #         f.write(b64decode(image))


elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')








