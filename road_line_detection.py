import cv2
import numpy as np


#resmi kesip interestini belirlemek için öncelikli maskeleme yapılır.
def region_of_interest(image,vertices):
    #image boyutu kadar sıfırlardan oluşan maske
    mask=np.zeros_like(image)
    
    match_mask_color=255
    
    #mask oluşturulan opencv fonksiyonu
    cv2.fillPoly(mask,vertices,match_mask_color)
    
    #piksel işlemi
    masked_image=cv2.bitwise_and(image,mask)
    
    return masked_image

#Line'ları çizdirmek görselleştirmek için
def drawLines(image,lines):
    image=np.copy(image)
    
    blank_image=np.zeros((image.shape[0],image.shape[1],3),dtype=np.uint8)
   
    for line in lines:
        for x1,y1,x2,y2 in line:
            #x1,y1 ve x2,y2 arsındaki yerleri doldur.
            cv2.line(blank_image,(x1,y1),(x2,y2),(0,255,0),
                     thickness=5)
            
    # Cizdirilen line orjinal resme eklenir.
    image=cv2.addWeighted(image,0.8,blank_image,1,0.0)
    
    return image
  
    
    

def process(image):
    
    #Videonun shape yükseklik ve genişlik olarak verilir.
    height,width=img.shape[0],img.shape[1]
    
    region_of_interest_vertices=[(0,height),(width,height),(width,0)]

    gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  
    
    #canny fonksiyonu çagrılır. Line detection için kullanılır.
    canny_image=cv2.Canny(gray_image,250,120)
    
    cropped_image = region_of_interest(canny_image, 
                                       np.array([region_of_interest_vertices], np.int32))
    
    #cropped edilen bölgelerde kalan line'ları tespit etmek için
    lines=cv2.HoughLinesP(cropped_image,
                    rho=2,
                    theta=np.pi/180,
                    threshold=220,
                    lines=np.array([]),
                    minLineLength=150,
                    maxLineGap=2)
    
    imagewithline=drawLines(image,lines)
  
    
    return imagewithline



cap=cv2.VideoCapture("../data/video1.mp4")



while True:
    
    success,img=cap.read()
    
    img=process(img)
    
    if success:
    
        cv2.imshow("image",img)
      
        if cv2.waitKey(20) &0xFF ==ord('q'):
            break
    else: break

cap.release()
cv2.destroyAllWindows()