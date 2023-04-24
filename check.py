import cv2
import os
sample=cv2.imread("SOCOFing\Real/100__M_Left_index_finger.BMP")

best_score=0
filename=None
image=None
kp1,kp2,mp=None,None,None
counter=0
for file in[file for file in os.listdir("SOCOFing\Real")][1:20]:
    if counter%1==0:
        print(counter)
        print(file)
    counter+=1
    fing_img=cv2.imread("SOCOFing\Real/"+file)
    sift=cv2.SIFT_create()

    keypoints_1,descriptors_1=sift.detectAndCompute(sample,None)
    keypoints_2,descriptors_2=sift.detectAndCompute(fing_img,None)

    matches=cv2.FlannBasedMatcher({"algorithm":1,"trees":10},{}).knnMatch(descriptors_1,descriptors_2,k=2)

    match_points=[]
    for p,q in matches:
        if p.distance<0.39*q.distance:
            match_points.append(p)
    
    keypoints=0
    if len(keypoints_1)<len(keypoints_2):
        keypoints=len(keypoints_1)
    else:
        keypoints=len(keypoints_2)

    if len(match_points)/keypoints*100>best_score:
        best_score=len(match_points)/keypoints*100
        filename=file
        image=fing_img
        kp1,kp2,mp=keypoints_1,keypoints_2,match_points
    
print("best matches:"+filename)
print("score:"+str(best_score))

result=cv2.drawMatches(sample,kp1,image,kp2,mp,None)
result=cv2.resize(result,None,fx=1.4,fy=1.4)
cv2.imshow("Result:",result)
cv2.waitKey(0)
cv2.destroyAllWindows()