# Table of Contents

- [1 metrics](#1-metrics)
  - [1.1 F1\_Score](#11-f1\_score)
  - [1.2 FN](#12-fn)
  - [1.3 FP](#13-fp)
  - [1.4 FPR](#14-fpr)
  - [1.5 TN](#15-tn)
  - [1.6 TP](#16-tp)
  - [1.7 TPR](#17-tpr)
  - [1.8 confusion\_matrix](#18-confusion\_matrix)
  - [1.9 plot\_confusion\_matrix](#19-plot\_confusion\_matrix)
  - [1.10 precision](#110-precision)
  - [1.11 recall](#111-recall)
  - [1.12 top\_10\_accuracy](#112-top\_10\_accuracy)
  - [1.13 top\_1\_accuracy](#113-top\_1\_accuracy)
  - [1.14 top\_2\_accuracy](#114-top\_2\_accuracy)
  - [1.15 top\_3\_accuracy](#115-top\_3\_accuracy)
  - [1.16 top\_5\_accuracy](#116-top\_5\_accuracy)
  - [1.17 top\_k\_accuracy](#117-top\_k\_accuracy)
- [2 model](#2-model)
  - [2.2 Constants](#22-constants)
  - [2.1 load\_model](#21-load\_model)
- [3 multi\_transforms](#3-multi\_transforms)
  - [3.1 BGR2GRAY : MultiTransform](#31-bgr2gray--multitransform)
    - [3.1.1 \_\_call\_\_](#311-\_\_call\_\_)
    - [3.1.2 \_\_init\_\_](#312-\_\_init\_\_)
  - [3.2 BGR2RGB : MultiTransform](#32-bgr2rgb--multitransform)
    - [3.2.1 \_\_call\_\_](#321-\_\_call\_\_)
    - [3.2.2 \_\_init\_\_](#322-\_\_init\_\_)
  - [3.3 Brightness : MultiTransform](#33-brightness--multitransform)
    - [3.3.1 \_\_call\_\_](#331-\_\_call\_\_)
    - [3.3.2 \_\_init\_\_](#332-\_\_init\_\_)
  - [3.4 CenterCrop : MultiTransform](#34-centercrop--multitransform)
    - [3.4.1 \_\_call\_\_](#341-\_\_call\_\_)
    - [3.4.2 \_\_init\_\_](#342-\_\_init\_\_)
  - [3.5 Color : MultiTransform](#35-color--multitransform)
    - [3.5.1 \_\_call\_\_](#351-\_\_call\_\_)
    - [3.5.2 \_\_init\_\_](#352-\_\_init\_\_)
  - [3.6 Compose : builtins.object](#36-compose--builtinsobject)
    - [3.6.1 \_\_call\_\_](#361-\_\_call\_\_)
    - [3.6.2 \_\_init\_\_](#362-\_\_init\_\_)
  - [3.7 GaussianNoise : MultiTransform](#37-gaussiannoise--multitransform)
    - [3.7.1 \_\_call\_\_](#371-\_\_call\_\_)
    - [3.7.2 \_\_init\_\_](#372-\_\_init\_\_)
  - [3.8 MultiTransform : builtins.object](#38-multitransform--builtinsobject)
    - [3.8.1 \_\_call\_\_](#381-\_\_call\_\_)
    - [3.8.2 \_\_init\_\_](#382-\_\_init\_\_)
  - [3.9 Normalize : MultiTransform](#39-normalize--multitransform)
    - [3.9.1 \_\_call\_\_](#391-\_\_call\_\_)
    - [3.9.2 \_\_init\_\_](#392-\_\_init\_\_)
  - [3.10 RGB2BGR : BGR2RGB](#310-rgb2bgr--bgr2rgb)
    - [3.10.1 \_\_call\_\_](#3101-\_\_call\_\_)
    - [3.10.2 \_\_init\_\_](#3102-\_\_init\_\_)
  - [3.11 RandomCrop : MultiTransform](#311-randomcrop--multitransform)
    - [3.11.1 \_\_call\_\_](#3111-\_\_call\_\_)
    - [3.11.2 \_\_init\_\_](#3112-\_\_init\_\_)
  - [3.12 RandomHorizontalFlip : MultiTransform](#312-randomhorizontalflip--multitransform)
    - [3.12.1 \_\_call\_\_](#3121-\_\_call\_\_)
    - [3.12.2 \_\_init\_\_](#3122-\_\_init\_\_)
  - [3.13 RandomVerticalFlip : MultiTransform](#313-randomverticalflip--multitransform)
    - [3.13.1 \_\_call\_\_](#3131-\_\_call\_\_)
    - [3.13.2 \_\_init\_\_](#3132-\_\_init\_\_)
  - [3.14 Resize : MultiTransform](#314-resize--multitransform)
    - [3.14.1 \_\_call\_\_](#3141-\_\_call\_\_)
    - [3.14.2 \_\_init\_\_](#3142-\_\_init\_\_)
  - [3.15 Rotate : MultiTransform](#315-rotate--multitransform)
    - [3.15.1 \_\_call\_\_](#3151-\_\_call\_\_)
    - [3.15.2 \_\_init\_\_](#3152-\_\_init\_\_)
  - [3.16 Satturation : MultiTransform](#316-satturation--multitransform)
    - [3.16.1 \_\_call\_\_](#3161-\_\_call\_\_)
    - [3.16.2 \_\_init\_\_](#3162-\_\_init\_\_)
  - [3.17 Scale : MultiTransform](#317-scale--multitransform)
    - [3.17.1 \_\_call\_\_](#3171-\_\_call\_\_)
    - [3.17.2 \_\_init\_\_](#3172-\_\_init\_\_)
  - [3.18 Stack : MultiTransform](#318-stack--multitransform)
    - [3.18.1 \_\_call\_\_](#3181-\_\_call\_\_)
    - [3.18.2 \_\_init\_\_](#3182-\_\_init\_\_)
  - [3.19 ToCVImage : MultiTransform](#319-tocvimage--multitransform)
    - [3.19.1 \_\_call\_\_](#3191-\_\_call\_\_)
    - [3.19.2 \_\_init\_\_](#3192-\_\_init\_\_)
  - [3.20 ToNumpy : MultiTransform](#320-tonumpy--multitransform)
    - [3.20.1 \_\_call\_\_](#3201-\_\_call\_\_)
    - [3.20.2 \_\_init\_\_](#3202-\_\_init\_\_)
  - [3.21 ToPILImage : MultiTransform](#321-topilimage--multitransform)
    - [3.21.1 \_\_call\_\_](#3211-\_\_call\_\_)
    - [3.21.2 \_\_init\_\_](#3212-\_\_init\_\_)
  - [3.22 ToTensor : MultiTransform](#322-totensor--multitransform)
    - [3.22.1 \_\_call\_\_](#3221-\_\_call\_\_)
    - [3.22.2 \_\_init\_\_](#3222-\_\_init\_\_)
- [4 run](#4-run)
  - [4.1 Run : builtins.object](#41-run--builtinsobject)
    - [4.1.1 \_\_init\_\_](#411-\_\_init\_\_)
    - [4.1.2 append](#412-append)
    - [4.1.3 get\_avg](#413-get\_avg)
    - [4.1.4 get\_val](#414-get\_val)
    - [4.1.5 len](#415-len)
    - [4.1.6 load\_best\_state\_dict](#416-load\_best\_state\_dict)
    - [4.1.7 load\_state\_dict](#417-load\_state\_dict)
    - [4.1.8 pickle\_dump](#418-pickle\_dump)
    - [4.1.9 pickle\_load](#419-pickle\_load)
    - [4.1.10 plot](#4110-plot)
    - [4.1.11 recalculate\_moving\_average](#4111-recalculate\_moving\_average)
    - [4.1.12 save](#4112-save)
    - [4.1.13 save\_best\_state\_dict](#4113-save\_best\_state\_dict)
    - [4.1.14 save\_state\_dict](#4114-save\_state\_dict)


# 1 metrics

[TOC](#table-of-contents)

## 1.1 F1\_Score

[TOC](#table-of-contents)

**Description**

F1 Score. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

F1 Score : float

**Equations**

$precision = \frac{TP}{TP + FP}$

$recall = \frac{TP}{TP + FN}$

$F_1 = \frac{2 \cdot precision \cdot recall}{precision + recall} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$



**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

f1score = m.F1_Score(Y, T)

print(f1score) --> 0.5
```

## 1.2 FN

[TOC](#table-of-contents)

**Description**

False negatives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

False negatives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fn = m.FN(Y, T)
print(fn) -> 1
```

## 1.3 FP

[TOC](#table-of-contents)

**Description**

False positives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

False positives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fp = m.FP(Y, T)
print(fp) -> 1
```

## 1.4 FPR

[TOC](#table-of-contents)

**Description**

False positive rate. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

False positive rate : float

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

fpr = m.FPR(Y, T)
print(fpr) -> 0.08333333333333333
```

## 1.5 TN

[TOC](#table-of-contents)

**Description**

True negatives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

True negatives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tn = m.TN(Y, T)
print(tn) -> 11
```

## 1.6 TP

[TOC](#table-of-contents)

**Description**

True positives. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

True positives : int

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tp = m.TP(Y, T)
print(tp) -> 5
```

## 1.7 TPR

[TOC](#table-of-contents)

**Description**

True positive rate. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

True positive rate : float

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

tpr = m.TPR(Y, T)
print(tpr) -> 0.8333333333333334
```

## 1.8 confusion\_matrix

[TOC](#table-of-contents)

**Description**

Calculates the confusion matrix. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Confusion matrix : torch.Tensor

**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

conf_mat = m.confusion_matrix(Y, T)
print(conf_mat) -> tensor([
  [1, 1, 0],
  [0, 2, 0],
  [0, 0, 2]
])
```

## 1.9 plot\_confusion\_matrix

[TOC](#table-of-contents)

**Description**

Plot the confusion matrix

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| confusion_matrix | torch.Tensor | Confusion matrix |
| labels | str, optional, default = None | Class labels -> automatic labeling C000, ..., CXXX if labels is None |
| cmap | str, optional, default = 'Blues' | Seaborn cmap, see https://r02b.github.io/seaborn_palettes/ |
| xlabel | str, optional, default = 'Predicted label' | X-Axis label |
| ylabel | str, optional, default = 'True label' | Y-Axis label |
| title | str, optional, default = 'Confusion Matrix' | Title of the plot |
| plt_show | bool, optional, default = False | Set to True to show the plot |
| save_file_name | str, optional, default = None | If not None, the plot is saved under the specified save_file_name. |

**Returns**

Image of the confusion matrix : np.array

![](documentation/image/confusion_matrix.jpg)
## 1.10 precision

[TOC](#table-of-contents)

**Description**

Precision. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Precision : float

**Equations**

$precision = \frac{TP}{TP + FP}$



**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

precision = m.precision(Y, T)
print(precision) -> 0.8333333333333334
```

## 1.11 recall

[TOC](#table-of-contents)

**Description**

Recall. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Recall : float

**Equations**

$recall = \frac{TP}{TP + FN}$



**Example**

```python
import rsp.ml.metrics as m
import torch

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

recall = m.recall(Y, T)
print(recall) -> 0.8333333333333334
```

## 1.12 top\_10\_accuracy

[TOC](#table-of-contents)

**Description**

Top 10 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 10 accuracy -> top k accuracy | k = 10 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_10_accuracy = m.top_10_accuracy(Y, T, k = 3)

print(top_10_accuracy) --> 1.0
```

## 1.13 top\_1\_accuracy

[TOC](#table-of-contents)

**Description**

Top 1 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 1 accuracy -> top k accuracy | k = 1 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_1_accuracy = m.top_1_accuracy(Y, T, k = 3)

print(top_1_accuracy) --> 0.8333333333333334
```

## 1.14 top\_2\_accuracy

[TOC](#table-of-contents)

**Description**

Top 2 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 2 accuracy -> top k accuracy | k = 2 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_2_accuracy = m.top_2_accuracy(Y, T, k = 3)

print(top_2_accuracy) --> 1.0
```

## 1.15 top\_3\_accuracy

[TOC](#table-of-contents)

**Description**

Top 3 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 3 accuracy -> top k accuracy | k = 3 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_3_accuracy = m.top_3_accuracy(Y, T, k = 3)

print(top_3_accuracy) --> 1.0
```

## 1.16 top\_5\_accuracy

[TOC](#table-of-contents)

**Description**

Top 5 accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top 5 accuracy -> top k accuracy | k = 5 : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_5_accuracy = m.top_5_accuracy(Y, T, k = 3)

print(top_5_accuracy) --> 1.0
```

## 1.17 top\_k\_accuracy

[TOC](#table-of-contents)

**Description**

Top k accuracy. Expected input shape: (batch_size, num_classes)

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| Y | torch.Tensor | Prediction |
| T | torch.Tensor | True values |

**Returns**

Top k accuracy : float

**Example**

```python
import rsp.ml.metrics as m

Y = torch.tensor([
  [0.1, 0.1, 0.8],
  [0.03, 0.95, 0.02],
  [0.05, 0.9, 0.05],
  [0.01, 0.87, 0.12],
  [0.04, 0.03, 0.93],
  [0.94, 0.02, 0.06]
])
T = torch.tensor([
  [0, 0, 1],
  [1, 0, 0],
  [0, 1, 0],
  [0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]
])

top_k_accuracy = m.top_k_accuracy(Y, T, k = 3)

print(top_k_accuracy) --> 1.0
```

# 2 model

[TOC](#table-of-contents)

## 2.2 Constants

[TOC](#table-of-contents)

| Name | Value | Description |
| -----|-------|------------ |
| TUC_ActionPrediction_model004 | TUC/ActionPrediction/Model4 | **TUC Action prediction model 4**<br>CNN with Multihead-Self-Attention<br>**Input**<br>- batch size<br>- sequence length = 30<br>- channels = 3<br>- width = 200<br>- height = 200<br>**Output**<br>- batch size<br>- number of classes = 10 |
| TUC_ActionPrediction_model005 | TUC/ActionPrediction/Model5 | **TUC Action prediction model 5**<br>CNN with Multihead-Self-Attention<br>**Input**<br>- batch size<br>- sequence length = 30<br>- channels = 3<br>- width = 300<br>- height = 300<br>**Output**<br>- batch size<br>- number of classes = 10 |
| URL | https://drive.google.com/drive/folders/1ulNnPqg-5wvenRl2CuJMxMMcaiYfHjQ9?usp=share_link | Google Drive URL |


## 2.1 load\_model

[TOC](#table-of-contents)

**Description**

Loads a model from an pretrained PyTorch external source into memory.

> See Constants for available models

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| model_id | str | ID of the model |
| force_reload | bool | Overwrite local file -> forces downlad. |

**Returns**

Pretrained PyTorch model : torch.nn.Module

**Example**

```python
import rsp.ml.model as model

model004 = model.load_model(model.TUC_ActionPrediction_model004)
```

# 3 multi\_transforms

[TOC](#table-of-contents)

## 3.1 BGR2GRAY : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a sequence of BGR images to grayscale images


### 3.1.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.1.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.2 BGR2RGB : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.2.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.2.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.3 Brightness : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.3.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.3.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.4 CenterCrop : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.4.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.4.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.5 Color : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.5.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.5.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.6 Compose : builtins.object

[TOC](#table-of-contents)

**Description**

Composes several MultiTransforms together.

**Example**

```python
import rsp.ml.multi_transforms as t

transforms = t.Compose([
  t.BGR2GRAY(),
  t.Scale(0.5)
])
```
### 3.6.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

### 3.6.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| children | List[MultiTransform] | List of MultiTransforms to compose. |
## 3.7 GaussianNoise : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.7.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.7.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.8 MultiTransform : builtins.object

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.8.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.8.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.9 Normalize : MultiTransform

[TOC](#table-of-contents)

**Description**

Normalize images with mean and standard deviation. Given mean: (mean[1],...,mean[n]) and std: (std[1],..,std[n]) for n channels, this transform will normalize each channel of the input torch.*Tensor i.e., output[channel] = (input[channel] - mean[channel]) / std[channel]

> Based on torchvision.transforms.Normalize


### 3.9.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.9.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| mean | List[float] | Sequence of means for each channel. |
| std | List[float] | Sequence of standard deviations for each channel. |
| inplace | bool | Set to True make this operation in-place. |
## 3.10 RGB2BGR : BGR2RGB

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.10.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.10.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.11 RandomCrop : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.11.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.11.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Test

## 3.12 RandomHorizontalFlip : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.12.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.12.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.13 RandomVerticalFlip : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.13.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.13.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.14 Resize : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.14.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.14.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.15 Rotate : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.15.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.15.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.16 Satturation : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.16.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.16.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.17 Scale : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.17.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.17.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.18 Stack : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.18.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.18.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.19 ToCVImage : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.19.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.19.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.20 ToNumpy : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.20.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.20.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.21 ToPILImage : MultiTransform

[TOC](#table-of-contents)

**Description**

MultiTransform is an extension to keep the same transformation over a sequence of images instead of initializing a new transformation for every single image. It is inspired by `torchvision.transforms` and could be used for video augmentation. Use `rsp.ml.multi_transforms.Compose`to combine multiple image sequence transformations.

> **Note** `rsp.ml.multi_transforms.MultiTransform` is a base class and should be inherited.


### 3.21.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.21.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

## 3.22 ToTensor : MultiTransform

[TOC](#table-of-contents)

**Description**

Converts a sequence of images to torch.Tensor.


### 3.22.1 \_\_call\_\_

[TOC](#table-of-contents)

**Description**

Call self as a function.

**Parameters**

| Name | Type | Description |
|------|------|-------------|
| input | torch.Tensor<br>List[PIL.Image]<br>List[numpy.array] | Sequence of images |
### 3.22.2 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initializes a new instance.

# 4 run

[TOC](#table-of-contents)

## 4.1 Run : builtins.object

[TOC](#table-of-contents)


### 4.1.1 \_\_init\_\_

[TOC](#table-of-contents)

**Description**

Initialize self.  See help(type(self)) for accurate signature.

### 4.1.2 append

[TOC](#table-of-contents)

### 4.1.3 get\_avg

[TOC](#table-of-contents)

### 4.1.4 get\_val

[TOC](#table-of-contents)

### 4.1.5 len

[TOC](#table-of-contents)

### 4.1.6 load\_best\_state\_dict

[TOC](#table-of-contents)

### 4.1.7 load\_state\_dict

[TOC](#table-of-contents)

### 4.1.8 pickle\_dump

[TOC](#table-of-contents)

### 4.1.9 pickle\_load

[TOC](#table-of-contents)

### 4.1.10 plot

[TOC](#table-of-contents)

### 4.1.11 recalculate\_moving\_average

[TOC](#table-of-contents)

### 4.1.12 save

[TOC](#table-of-contents)

### 4.1.13 save\_best\_state\_dict

[TOC](#table-of-contents)

### 4.1.14 save\_state\_dict

[TOC](#table-of-contents)

