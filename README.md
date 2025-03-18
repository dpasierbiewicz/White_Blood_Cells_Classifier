# White_Blood_Cells_Classifier

This project aimed to develop software capable of classifying images of single leukocytes that are stained into five categories: **lymphocytes**, **monocytes**, **neutrophils**, **eosinophils** and **basophils**, utilizing a convolutional neural network.

---

##  Datasets  
The project dataset consists of white blood cells images from two online image datasets, which were combined into one.

### 1. **Dataset for Microscopic Peripheral Blood Cell Images[1]**  
- **Source**: [Click here](https://data.mendeley.com/datasets/snkd93bnjr/1) 
- **Description**:  
  - Original dataset contains **17 092** images across **8 cell groups**.  
 - **Subsets used**:
   - Neutrophils, eosinophils, basophils, lymphocytes, and monocytes (total **10 298** images).  
   - Excluded classes: Immature granulocytes, erythroblasts, and platelets.  

### 2. **Raabin-WBC: Double-Labeled Cropped Cells[2]**  
- **Source**: [Click here](https://www.nature.com/articles/s41598-021-04426-x)  
- **Description**:  
  - Subset of the Raabin-WBC dataset, which contains **17 965** images and three subsets.  
 - **Subsets used**:  
    - **Train** and **Test-A** splits (covers all 5 target classes), which contains **14 514** images.  
    - **Test-B** excluded (contains only low quality images of neutrophils and lymphocytes).  

---

### Dataset Summary  

- **Total images**: 24,812  
- **Split**:  
  | Subset      | Images  | Percentage |  
  |:-------------:|:---------:|:------------:|  
  | Train       | 18,412  | 74.2%      |  
  | Validation  | 3,200   | 12.9%      |  
  | Test        | 3,200   | 12.9%      |
- **Class Distribution**:  
  | Subset      | Neutrophils [%] | Eosinophils [%] | Basophils [%] | Monocytes [%] | Lymphocytes [%] |  
  |:-------------:|:-----------------:|:-----------------:|:---------------:|:---------------:|:-----------------:|  
  | Train       | 48.3            | 17.6            | 6.4           | 9.2           | 18.5            |  
  | Validation  | 52.0            | 14.8            | 5.2           | 8.1           | 20.0            |  
  | Test        | 52.0            | 14.8            | 5.2           | 8.1           | 20.0            |  

About **50%** of all images are Neutrophils, the least amount of images are basophils and monocytes, but because of huge amount of images every subset has over **100 images**.


---

###  License  
Both datasets are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.  
- Learn more: [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/).  


---

 ### Citations 
[1] Acevedo, Andrea; Merino, Anna; Alférez, Santiago; Molina, Ángel; Boldú, Laura; Rodellar, José (2020), “A dataset for microscopic peripheral blood cell images for development of automatic recognition systems”, Mendeley Data, V1, doi: 10.17632/snkd93bnjr.1
[2]  Kouzehkanan, Z.M., Saghari, S., Tavakoli, S. _et al._ A large dataset of white blood cells containing cell locations and types, along with segmented nuclei and cytoplasm. _Sci Rep_  **12**, 1123 (2022). https://doi.org/10.1038/s41598-021-04426-x
