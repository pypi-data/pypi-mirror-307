#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : ecraft
# @Time         : 2024/10/31 16:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.io.files_utils import to_url
from meutils.schemas.image_types import ImageRequest, ImagesResponse, RecraftImageRequest
from meutils.notice.feishu import IMAGES, send_message as _send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling, aget_spreadsheet_values
from meutils.decorators.retry import retrying

BASE_URL = "https://api.recraft.ai"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=Lrhtf2"

DEFAULT_MODEL = "recraftv3"
MODELS = {}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)


@alru_cache(ttl=10 * 60)
@retrying()
async def get_access_token(token: Optional[str] = None):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
    headers = {"cookie": token}

    async with httpx.AsyncClient(base_url="https://www.recraft.ai", headers=headers, timeout=60) as client:
        response = await client.get("/api/auth/session")
        response.raise_for_status()
        logger.debug(response.json())
        return response.json()["accessToken"]


# @retrying()
async def generate(request: RecraftImageRequest, token: Optional[str] = None):
    token = await get_access_token(token)
    headers = {"Authorization": f"Bearer {token}"}
    # params = {"project_id": "26016b99-3ad0-413b-821b-5f884bd9454e"}  # project_id 是否是必要的
    params = {}  # project_id 是否是必要的
    # params = {"project_id": "47ba6825-0fde-4cea-a17e-ed7398c0a298"}
    payload = request.model_dump(exclude_none=True)
    logger.debug(payload)

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
        response = await client.post(f"/queue_recraft/prompt_to_image", params=params, json=payload)
        response.raise_for_status()
        params = {
            "operation_id": response.json()["operationId"]
        }
        logger.debug(params)

        response = await client.get("/poll_recraft", params=params)
        response.raise_for_status()
        metadata = response.json()
        logger.debug(metadata)

        # {'credits': 1,
        #  'height': 1024,
        #  'images': [{'image_id': 'f9d8e7dd-c31f-4208-abe4-f44cdff050c2',
        #              'image_invariants': {'preset': 'any'},
        #              'transparent': False,
        #              'vector_image': False}],
        #  'random_seed': 1423697946,
        #  'request_id': '77bd917d-0960-4921-916f-038c773a41fd',
        #  'transform_model': 'recraftv3',
        #  'width': 1024}

        params = {"raster_image_content_type": "image/webp"}  #####
        params = {"raster_image_content_type": "image/png"}

        images = []
        for image in response.json()["images"]:
            response = await client.get(f"""/image/{image["image_id"]}""", params=params)
            url = await to_url(response.content)
            images.append(url)

        return ImagesResponse(image=images, metadata=metadata)


async def check_token(token, threshold: float = 1):
    if not isinstance(token, str):
        tokens = token
        r = []
        for batch in tqdm(tokens | xgroup(32)):
            bools = await asyncio.gather(*map(check_token, batch))
            r += list(itertools.compress(batch, bools))
        return r
    try:
        access_token = await get_access_token(token)
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=60) as client:
            response = await client.get("/users/me")
            response.raise_for_status()
            data = response.json()
            logger.debug(data["credits"])
            return data["credits"] >= threshold
    except Exception as e:
        logger.error(e)
        logger.debug(token)
        return False


if __name__ == '__main__':
    token = None
    # arun(get_access_token())
    request = RecraftImageRequest(
        prompt='一条猫'
    )
    # arun(generate(request, token=token))

    tokens = list(arun(aget_spreadsheet_values(feishu_url=FEISHU_URL, to_dataframe=True))[0]) | xfilter_

    # tokens = "AMP_7268c9db0f=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2OTE1YzI1My1jMTJjLTQ5ODYtYjM3Ni0xMTI3Y2ZmMTFlMjglMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI0MDQ5YWRmMi0yNWQ0LTRkNmUtYTFkMy01YmY3NmI3NDMwZDElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzMwNDQ1NTg2NDcwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczMDQ0OTY4MzM0NyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjUlMkMlMjJwYWdlQ291bnRlciUyMiUzQTEyJTdE;__zlcmid=1OVn8OoYVNvKEWM;AMP_MKTG_7268c9db0f=JTdCJTdE;_ga=GA1.1.435165527.1730362257;__Secure-next-auth.session-token.1=ML_bnTrrKhsDvITN8h4reDgB4vgI5XYeDZqsg4Toc04ODZcRFADRtpfQuaRqWG1i22Ki2-WehfPVmu5AMJCN-1YjaRZUbB9N1v77h97YDKyVREJqB6PsbDOPL8zVxSdeup_dHNRD72gSacb-5liVtBLz8-gC5k_36AHkiqQazMY3phd6IHSi9BHrPKd1yc6L4MUX9cB1pysuWuSrgpr3ivgECA5RBUEtDhhmey18m_UnO4Bew1ignPHapwzuG4ZDufTNM_q-gCbo2gppm741--WGkJMvrnNf9EJNzaE3PaLts_QL7DB5MmauE5LlhYdjkEJRFkfxPFIac4mANldMLNNvCOWFyOvmrzWR8NTDvGsZTkyOehuCFEOhG8kShjtL3RJSXO2lEELO9MVVjxSoey_6l-wmgY6hwS_5zRXaEztgulYAH8ar4CV0Z7t4PcV8ukzkgbZ1-jP6lo9DeKP9yGlWfNXAgDU_5_1VIwmhFNshBgt3vpZ06hHyY-uoKWRLlOjMCpcOi6HO8zRDTAP_j_88rOQo5DU4GBxtzXPkFY6utD6zccrUDw0gmTmeJhHBZIGZFwFnkyAMaiQL8jGWCMw.ExRFqvq_EKdb5IsViyRlSA;_uetsid=a8a77260975f11ef834045ac9f7830ad;__Host-next-auth.csrf-token=78920fc4c6bf5aef5c2063e3a4397b1e41074713e35020cf7049156e02d53355%7C2c8e6897101210b68ba31cec5c6232d8ab76a3e070cda7b82ad051680ab93fe0;_ga_ME15C3DGRL=GS1.1.1730445586.7.1.1730449683.0.0.0;_fbp=fb.1.1730362257600.714008794112161913;_pin_unauth=dWlkPU0yWmxPR1JsWkRJdE5qZGlZeTAwTWpNeUxXRmpNVEV0TlRrd1l6RTNZelEwTldZMw;x-recraft-referral-code=3h7wfOgFGn;__Secure-next-auth.callback-url=https%3A%2F%2Fwww.recraft.ai%2Fprojects;__Secure-next-auth.session-token.0=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..xVLyHXt0LQCGPXrw.CtP1obq0K9V9NuXa2mjRIt0TnNe-StiIcgfp5N6-agDvLVqHz8pBlLQ4mDEau9fy-fLBKqmpqx3Wc4kEaJwQ116PZxrqkXShbzkz1Qaz-8DuYhSL4EvFMTAkROvdukaiFLRKYPnl2d30Ize7VGp5Wir_OkenVZnDr5kyI4NyqpVjHFAnX_0kzmQfOJqR2szMzte_w9zMmUWrqG_8hLArm3reA6DsmmJMeGj9-3MZo7inrmfM4FQ7mBVrNadw5uw14yh32ATXn4470idM8RvBTrlWSbAuTOBpXy5Cwp2RPqKfaXnBYyqH7WRpEJZyKdHUWY0VYGf47w37hLG7aT0wuq_eIRJvHHkxah6-96ugmxjV25OGfwLmyNXpySh77JP23dsbkWq2lBUGNc6q-RlxgsLV-fKsPe5FBGpOqoMjlD_zG7k-Ne0DQ66xfm_zGetUmcp7q1LQ81a-egOVAEGAFnLz5K0hyJ_c8pR4tSJ2c2MTt2_ZjeFs07Y33NZVY4SlUPCiGGRRAuY8gE56pCwBdchK64FtSf3qbT04dvyDc26iJJVcLb_jQUclw6JCg8klW-v61rV4u8J4jtTo-3Cw59XHV0nuMozfa08XtOe2qAbRLk6C5Jtg-xjQevJPNENGz75NBd_QZD422lO5Ay7934dFOTjABrvvA-J3xCi2lKRd5HY3Cc4bY-r0I0z_jXi50-M5MUXbenves0bo7Lg4DYzYyQV83AGFv8bmk3VMMrco10qonZyvxsPkOAQcvPjZMiaCYTvdav_oc-u_LUtCRkdCXciHdhu4HCNvNEdNXbSEFoeq1jVqnQHeXKvcZOacwQ6gse_UnQYfEN_zCYTC7tLbBjMIGtqiWtBKmNFPfaZbkx9RiWosvUeu_J2y4py_VNW6Oxy74Uu31BP10ufHVwzJCykfWQ3o_DhxS5ziqoL0uGZsPnSFe-Tgxf0I424Th3ct-4TVb4MRensrM4zfglyrDdFG52-WYPjUEpIbf059L38pQ51eF_t5mDGWJdZD09kesPD_c31wQy1-dmrSkoaL300AHpikdECo0XwgAeMQlccYM6Y3Q0HWScyHcz8OpxqdbfsMJf33JIhmiEBwrKNyY66PxGXu74esbF57WQjiUjintqrle6B9D5ovqo_oDXWGZdgmJf76YPJ0_rt-Jx7YrsYSHax4wgJa-lUwXQo0wKlyhXPgAiEYO4YsPzOPYJGmV5kBDhzVzFDZ_xrS-WNYx2peWX_HD-37rr_c3NOl65zNUEmLJ4X1dcZo82Tho8aA-ADV--zC-Qoq0xNjDEYuuPYy0dq-3ECh4knWUCwWzkSOjoG-VdZertqhrekE4ShiOqG_KeiWeTw5jh_FqYzEMHvenNJ4VncGmrtg9nMfK4ohoqYvLOoIXLOnvFfueX_E3ZqaX3tg2KyRzRe_4acJC2VCE5m7jmoUqlFHK8y1ZNVdmvEbSNmrfdKbPdByfR495_I9ejjPXdGeBApPg-Z6RHEVAzJMto513PrZ3N1MtVy85YjeGFP9j5DPZDC6wo1rpo7wrCouyZrWhodSn1MxntIpDX0x2dBs72ETQfWpnpRi3BLlox_24MVU_ekrKOQmOkPPcAwRe4o9mDiOrYttFiq2JfsVPCcvuAfIkh8O3taXhImPTMPiETGsmVCzHrOuN6hIGUDzTVcPICqGpD55zgc-31ACiNByPRJnP-QwJHguyaAS1wc-zGFtORsbQmqJvhxjIV1IuuQyqjEl_NBBkMPXE4X8PFtjauYK6tnLxgA53-jMORLSQ9fkRUt0EcvxJfhbtooqYMskCAweUYFIdioKnemBhiDlWNIHXn8MCAP70MQPvA9B-84fK1_vNoeo-EflzzeD6375HwZtbc1HuN6Q_gbqdxneGQIUv6NfMIoAOJrdPpHSNEyKYfvRVhDcvWo3ecSWMXzn2IAxEZ4RKCcvEfwNFpRVVTpbUalF_GmPPSw_XDfYGPOFufZpeh8nx375G5GvfReSfacu1wGBRI3C9OYoyJPKGjC267LpArEHbwLoRDG6UmQeqLfNaBXmRO2d4lx17OePFojJ5tX6vRee5pT_CqQSkD8JJPLU2DTQVQNAD5ybOCqTizkIYfvZiEGVK22tkvilBm7q3cjI3gHSKMnwBKm4U2OgG8XkGzrT3bx9mMcRtEcw3u_t1TreuycePMtZgJ0R-8Hezq2EzaszZLNFJx4z6Lo7YS-yhPB5Eu4_e5MZEoMlsJzkBeEOs1dvObVDWBvBEriCfKjpci7n0C2NkRIazaqxFIt7lLDI14ah1ykd_FfDN7Qp7vsq1oEyUCU_nqhmKEeNNGh5Iv8gviVzZCvhTnG3I217IY6w0zsW3sE0rTtXnlIYby7iFaQrkUZ0Y0AuC7ZJH8KahhoonLLS6JTvyw3jsKgcpzHG_3ZFUDRh6YF4YXpVQROPo-uTbEvLb9ksR4z0AYXzDzzkuNf3Ua75I_c7Gdml4rf3vpcUBGhpzz0T1v_eWEO3sGeT84SF8700-pyR1mjFMHKDbE_BCnpNm564NsOcPWa9dR5Q8e3GCr3r9tE0Vd2RRiuYldNjakhMpmHE8GP-Z2W9tu_i_lH0c6ta3H0Wc0JWf8JvQ6agCbthT5unpANZvy7vt6lASh3Hc0e27AbvL-S5l7kI5vs04R7z42wacKs2jH5ottOXa3MFZk4k-zfv7XhfDLNIWpfbCO26cAwe7byv27JG_gHASjeJRj7bhKf5K6TJk4epK6fIss7Lmx9fNQpd1UDCWwe5rFaJguFS71-GCR_x1jYwmtYknYZ52tFKkdJVh_AlYESBDMKRyRQLTgif64IJwMDp-2HTvbEMafr9nMVMtwp34MJ8rSqf6ME4Dz8Wk-J5IP-LFf7TsvevAVpRLp1zUu3jD5C2piIRiVn4asYPes6eqaXHIaQw111m6SyZbfxBrYStOBOvSgMUCxpSn5WdL8TVEO-6fdhvvY4gaEMkifq8URru93j2EJJyyvZ0_vpn0nSE9YKHv9a3okPHsKrm_bDD5rOSSyv_UeNqHvyxfZcTZyE4eqlihUUIJI1LsL2cu1Pv0wzHGqfP2FZAAYDq36Fjlj5LbrZQpOdgomlCRbABDlNyR4ip4V_dSzy_oL0E0LcitV0rDSA2nau7vOCRZOFPslrWUwBh6zooorIutHCWIGKpy8ZkkJ5_NuiXYrxMByurzBLgJb1rVrOtQQRSoypW_y4Aa4zr1gFISenRO7Ozrsvxe2LNGjvQM4ebXjBw5m49zaHXjMLOzjhchJY3ennDFsjwjd5GPqatswtliboXZ1M0Atigva4TxUO8OHKbuYwmk69yD5Bn_5DY2-rclnYcnWpngWOFXcCAXIluSnRJLriPk8sosTgUWvg0WenjyOhweUIootfTBSV2PqFWlXwcKVLFKFAEda0DpZWZYGnAv_Lfo7Y0vhwgVO0DK6DhM0cWfLmxg6GwwPlt8ngJ0DBOgd2TY3P-l1hieJ-r0yh-EILMuhzkuTVOigeoiiFYZ4nJc4oc2YNYLcO631AOmC0xWpzYpBYlEeDI8f7BLkrTfMBOzrryIAOYbvJYxNKLqFt94IyVNuTbrJBX98SZiJa5HaPCiC2dG60jwj76uVjTNPWaWg0rT_mYl4ArzkzAD1jwUUEhhzYmNmvM_h117lO-67I0EljOoAyuWYOdRauXxwhyYQRAdBTOZy5L8TK_xAkiTqcX5C43FUxXJEcB-GmnSxjgymOcZl9yXd1WtjO-be3KfjVqgltCZh_HhrF6ODTghJxwZtCq2dIn12_W431l8BG3z6a7lR0IU6qqjeIexA0D_2eYwH-1UGNjrswebUNBcqXpzGmdU-0yZ90u1DTv7tqJdSb74zWZZfi-_se;__stripe_mid=d21b2291-edb8-4cb1-8fac-05c6a9493ca8d85a3c;_clck=uflztg%7C2%7Cfqi%7C0%7C1765;_clsk=18ngmlp%7C1730449685636%7C56%7C1%7Cl.clarity.ms%2Fcollect;_gcl_au=1.1.906962865.1730362257;_tt_enable_cookie=1;_ttp=412qSInHGw3jjdyNR6K4tBIYmNZ;_uetvid=a8a766f0975f11ef9b7921e48a0cd258"
    arun(check_token(tokens))
