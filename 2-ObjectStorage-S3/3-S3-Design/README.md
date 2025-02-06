# Key entities

## Bucket. 
- A logical container for objects. 
- The bucket name is globally unique.

## Object. 
- Immutable data
  - To change data, upload a new version
  - Critical to maintain consistency and integrity of the data
- Metadata
  - Set of name-value pairs.
  - ```json
    {
      "data_blocks": [1,2,3,4],
      "name_or_key": "a.txt",
      "size": 123232434
    }
    ```

## Uniform Resource Identifier (URI).  
- Both bucket and object are resources


# Bucket creation

![](https://plantuml.online/uml/VPB1Ri8m38RlVGfhXmcaiTrxc4JNmv1WgWOyW4dDYDOcNU8YiQUVKsYqCB5J6_VxxJ-_YugjWwqdbtNeM2lTeM6uMrgieS06ZI9t1-XXMQJ4l5h0cjnHAng-opa55ZKPrdo2UvWhHTx32Wr-K2lbGR6OhrB5YXXhP4pwZiKRQ5aaL7dbihnkL_vfjPO4n1QysPfWKZdTeZjD1_Xo-8zVaxAcZefupB8GAioU9RWSNZUR2ghj9eSNHyW4krvz4iFJ-Japs5AsB08kEURmRdjJpvpTQGEEldhox84jy8420DBwA2iBhoAH87EOztomJd_J05r4C76seGVeR2F-oGEnUfnc8eYZHXsojc6OxwpnDBOUSxqstevRYOlu1PTouv3IRReiqkQnYm-o6YJ4lNRju2aPCLYE1HKy1Ti9Vx4USY_EyoCNhtVEEgmeXMIsxuU_TTytpUa7)

1. **User sends HTTP PUT request** to create a bucket named `/bucket-name`.
2. **Load Balancer** receives the request and forwards it to the **API Service** using round-robin.
3. **API Service** requests **IAM** to authorize the user.
4. **IAM** verifies user permissions and sends an **authorization response** to the API Service.
5. **API Service** requests **Metadata Service** to create bucket metadata.
6. **Metadata Service** stores the metadata in **Metadata DB**.
7. **Metadata DB** confirms metadata storage to **Metadata Service**.
8. **Metadata Service** confirms metadata creation to **API Service**.
9. **API Service** sends a **bucket creation response** to **Load Balancer**.
10. **Load Balancer** informs the user that the bucket was created successfully.


# Object creation

![](https://plantuml.online/uml/VLD1Ri8m4Bpd5IiE5KXDU-TGAMaEHOA26le0uop59R5Jsq6Yh-_QnA5EHM_OdfcTdGcCMwNXtQ1EMgQjuA9bqi9agLW5EQkPvAWdm0miynYHRHPGeZu9ZlwTpZ5WKQ6qmfxX3ZBEqHXOCSa-iA5hprXagvYnGiigPbca6ovlG8iyGXKZbyLOhlWZLL82P0jULOKmtMZHC7sUUN1_-0zV8bUo6XZ3CKbSg90-KN1pUDbkDx1PbzivF6ja5a7jFf5R418UTnq_eaqbQp1Pvev2MSxXJNMoIhNQ4KRZLuV66h0Ax04T04Z-HBMvdqIXCEUGTVQWjFX63-f9CDMgndjeLKqxe06q_66M464O5NZC2kM6cLP9Wq7QHJRodVXSwQrFwDQpLrzVLkKUKGNLqDWuaIOqE-M7JXwXLjpR2hw7vdzf51IngmN3h22IzFuWJGa-b3EsUzM9dGspZ1ElWEXxeHll9pBYznmk_AOkoGZVx-q-XzmtViKDYL_gTrzE3ABPflD_edrNr-SV)

1. **User sends HTTP POST request** to create an object in the bucket `/bucket-name`.
2. **Load Balancer** receives the request and forwards it to the **API Service** using round-robin.
3. **API Service** requests **IAM** to authorize the user.
4. **IAM** verifies user permissions and sends an **authorization response** to the API Service.
5. **API Service** requests **Data Service** to create the object.
6. **Data Service** creates the object on the **Primary Storage Node**.
7. **Data Service** confirms object creation to **API Service**.
8. **API Service** requests **Metadata Service** to create object metadata (e.g., chunk locations).
9. **Metadata Service** stores the object metadata in **Metadata DB**.
10. **Primary Storage Node** replicates the object to the **Secondary Storage Node**.
11. **Metadata DB** confirms metadata storage to **Metadata Service**.
12. **Metadata Service** confirms metadata creation to **API Service**.
13. **API Service** sends a **bucket creation response** to **Load Balancer**.
14. **Load Balancer** informs the user that the object was created successfully.


# Object download

https://plantuml.online/png/lPB1Ri8m38RlVGgBmmJIsEuzJ6fNQQi4enhm02QrIWOaNU8YiQTVKjgC3h7ZRhNzVtRwsoXO6rXRCb6DXgMGDIg6qKnZ2IdkKGao8q0BitIeI8eSbcIEKb1RT_5Ga9UaMF89xY0HWgo5EIgiwE3IBP4dyo4n9yOI6GTz--GDQPOELDclLsQ_ssLNhPRE0VSiUDCbmRWmye3cD6d5NV2NVab2gp8G8OmYRofCdvnnCRokLWKKY-KgXcT3o0Hwyq62GIfut3HYHpnLUA1ebdh4UHd3ksvKEJLwupI6FXkoR84ry9Qy05pxerkR_tI8CpE6fE6jDlABMb47mTZeFTr3hVVk7yW2iNYOH0u8eteEMMe_pDPQMUfRzzx6y48COjke7QpNUMQZi8M-qMMnexCX6MMTllFsijIbVgWX4RozP4Bo5lLVSywvfAeCLNx1RTM6SclFuhpqtXf_6LqgU7u-07yxLxLl

1. **User sends HTTP POST request** to create an object in the bucket `/bucket-name`.
2. **Load Balancer** receives the request and forwards it to the **API Service** using round-robin.
3. **API Service** requests **IAM** to authorize the user.
4. **IAM** verifies user permissions and sends an **authorization response** to the API Service.
5. **API Service** requests **Metadata Service** to get chunk UUIDs for the object.
6. **Metadata Service** provides the chunk UUIDs to the **API Service**.
7. **API Service** requests **Data Service** to retrieve the chunks.
8. **Data Service** retrieves chunks from the **Primary Storage Node**.
9. **Primary Storage Node** sends the chunks to the **Data Service**.
10. **Data Service** retrieves chunks from the **Secondary Storage Node**.
11. **Secondary Storage Node** sends the chunks to the **Data Service**.
12. **Data Service** aggregates the chunks to form the complete object.
13. **Data Service** sends the complete object to the **API Service**.
14. **API Service** sends the object response to the **Load Balancer**.
15. **Load Balancer** forwards the object response to the **User**.

### References
1. https://bytebytego.com/courses/system-design-interview
2. https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321