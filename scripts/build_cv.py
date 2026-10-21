"""Generate the public CV. Requires reportlab."""
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

ROOT=Path(__file__).resolve().parents[1]
INK=colors.HexColor('#263b31');ACCENT=colors.HexColor('#a34829');MUTED=colors.HexColor('#536052')
styles={
 'name':ParagraphStyle('name',fontName='Helvetica-Bold',fontSize=28,leading=32,textColor=INK,spaceAfter=9),
 'tag':ParagraphStyle('tag',fontName='Helvetica',fontSize=11,leading=16,textColor=ACCENT,spaceAfter=10),
 'contact':ParagraphStyle('contact',fontName='Helvetica',fontSize=9,leading=14,textColor=MUTED,spaceAfter=18),
 'section':ParagraphStyle('section',fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=ACCENT,spaceBefore=16,spaceAfter=10),
 'role':ParagraphStyle('role',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=INK,spaceAfter=3),
 'meta':ParagraphStyle('meta',fontName='Helvetica',fontSize=9,leading=13,textColor=MUTED,spaceAfter=7),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.5,leading=14.5,textColor=INK,spaceAfter=7),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=9.5,leading=14,textColor=INK,leftIndent=11,firstLineIndent=-10,spaceAfter=5),
 'paper':ParagraphStyle('paper',fontName='Helvetica',fontSize=9.2,leading=14,textColor=INK,spaceAfter=9),
}
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
for style in styles.values():
    style.fontName='DejaVu-Bold' if 'Bold' in style.fontName else 'DejaVu'
    if style.fontSize<12:
        style.fontSize-=.4
        style.leading-=.6
story=[]
def para(s,style='body'):story.append(Paragraph(s,styles[style]))
def section(s):para(s,'section')
def role(title,dates,bullets):
    story.append(KeepTogether([Paragraph(title,styles['role']),Paragraph(dates,styles['meta'])]))
    for b in bullets:para('- '+b,'bullet')
    story.append(Spacer(1,7))

para('ALI EL HABCHI','name')
para('Assistant Professor | Computer Vision &amp; Applied AI','tag')
para('Morocco &nbsp; | &nbsp; <link href="mailto:elhabchiali@gmail.com">elhabchiali@gmail.com</link><br/><link href="https://elhabchiali.github.io/">elhabchiali.github.io</link> &nbsp; | &nbsp; <link href="https://www.linkedin.com/in/ali-el-habchi/">linkedin.com/in/ali-el-habchi</link> &nbsp; | &nbsp; <link href="https://github.com/elhabchiali">github.com/elhabchiali</link>','contact')
para('AI researcher, engineer, and educator with a PhD in Computer Science and AI. Experience spans UAV perception, embedded inference, multilingual NLP, and production ML workflows. Teaching connects computer vision and software engineering with practical implementation.')
section('PROFESSIONAL EXPERIENCE')
role('Assistant Professor in AI &amp; Software Engineering | ENIAD Berkane','October 2025 - Present | Mohammed Premier University, Morocco',[
 'Teach image processing and computer vision, DevOps/MLOps, software modelling and UML, and related software engineering subjects.',
 'Develop practical coursework and demonstrations, supervise student projects, and participate in project evaluation and academic juries.'
])
role('Senior Machine Learning Engineer | Onclusive','May 2024 - September 2025 | Rabat, Morocco',[
 'Worked on multilingual NLP tasks including sentiment, named-entity recognition, topic detection, keyword extraction, clustering, and summarization.',
 'Contributed to transformer model migration and inference workflows, including tokenization, chunking, evaluation, quantization, and AWS-based pipelines.',
 'Worked with Python, Hugging Face and PyTorch, connecting model development with deployment and operational requirements.'
])
role('Machine Learning Engineering | Onclusive Social (formerly Digimind)','October 2023 - May 2024 | Morocco',[
 'Developed visual brand-analysis models using YOLOv5 for logo detection and ResNet50V2 for classification.',
 'Worked on dataset management and reproducible delivery using DVC, MLflow, GitLab CI, Docker, Kubernetes, and AWS.'
])
role('Senior R&amp;D / Computer Vision Engineer | ATLAN Space','August 2018 - September 2023 | Rabat, Morocco',[
 'Trained and deployed object detection and classification systems for aerial applications, including obstacles, vehicles, people, and boats.',
 'Implemented inference on Jetson Nano and Xavier AGX with OpenCV DNN, TensorRT and ONNX runtimes; developed C++ inference components.',
 'Developed optical-flow and multi-view approaches for obstacle perception and depth estimation, and target-geolocation software using OpenGL and terrain geometry.',
 'Contributed to drone software, communication and sensing components, photogrammetry workflows, and Azure-based development environments.'
])
story.append(PageBreak())
para('RESEARCH, EDUCATION &amp; PRACTICE','tag')
section('EDUCATION')
role('PhD in Computer Science &amp; Artificial Intelligence','2025 | ENSA Oujda, Mohammed Premier University',[
 'Doctoral research on UAV navigation through computer vision and deep learning, including obstacle perception, depth and motion cues, and aerial geolocation.'
])
para('<b>Master of Science in Software Engineering</b> | 2018<br/>Faculty of Sciences, Mohammed Premier University, Oujda')
para('<b>Licence in Mathematics and Informatics</b> | 2016<br/>Faculty of Sciences, Mohammed Premier University, Oujda')
section('SELECTED PUBLICATIONS')
publications=[
 ('2023','Evolutionary algorithm for optimized CNN architecture search applied to real-time boat detection in aerial images','Journal of Real-Time Image Processing 20, article 78. Co-author.','https://doi.org/10.1007/s11554-023-01332-5'),
 ('2022','Social distance monitoring using YoloV4 on aerial drone images','E3S Web of Conferences 351, 01035. First author.','https://www.e3s-conferences.org/articles/e3sconf/abs/2022/18/e3sconf_icies2022_01035/e3sconf_icies2022_01035.html'),
 ('2020','CGA: A New Approach to Estimate the Geolocation of a Ground Target from Drone Aerial Imagery','International Conference on Intelligent Computing in Data Sciences (ICDS). First author.','https://doi.org/10.1109/ICDS50568.2020.9268749'),
 ('2020','CNN Adaptations for Boat Detection in Aerial Images Tested on Yolo v2','International Symposium on Advanced Electrical and Communication Technologies (ISAECT). Co-author.','https://doi.org/10.1109/ISAECT50560.2020.9523704')
]
for year,title,venue,url in publications:para(f'<b>{year}</b> &nbsp; <link href="{url}">{title}</link><br/>{venue}','paper')
section('TECHNICAL PRACTICE')
para('<b>Learning &amp; perception:</b> Python, PyTorch, TensorFlow/Keras, OpenCV, NumPy, Hugging Face Transformers, object detection and classification, camera geometry, visual motion and depth.')
para('<b>Inference &amp; delivery:</b> TensorRT, ONNX, NVIDIA Jetson, quantization, AWS, Docker, Kubernetes, DVC, MLflow, GitLab CI, FastAPI.')
para('<b>Software &amp; geometry:</b> C++, Java, SQL, Git, Linux, OpenGL, software modelling and UML.')
section('SELECTED TRAINING &amp; LANGUAGES')
para('DevOps for Data Scientists (2023); Advanced AI: Transformers for Computer Vision (2023); Introduction to Generative AI (2023).')
para('<b>Arabic:</b> native &nbsp; | &nbsp; <b>French:</b> professional proficiency &nbsp; | &nbsp; <b>English:</b> professional proficiency')

def footer(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(colors.HexColor('#d7d9cd'));canvas.line(44,39,w-44,39)
    canvas.setFont('DejaVu',7);canvas.setFillColor(MUTED)
    canvas.drawString(44,26,'Ali El Habchi | Computer Vision & Applied AI')
    canvas.drawRightString(w-44,26,f'October 2026  /  {doc.page}')
    canvas.restoreState()

doc=SimpleDocTemplate(str(ROOT/'ali-el-habchi-cv.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=40,bottomMargin=52,title='Ali El Habchi - Computer Vision & Applied AI',author='Ali El Habchi')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
