# -*- coding: utf-8 -*-
import scrapy
import json

class RtsSpider(scrapy.Spider):
    name = 'rts-spider'
    allowed_domains = ['rts-tender.rum']
    start_urls = ['https://i.rts-tender.ru/main/auction/Trade/Privatization/View.aspx?Id=2221#3188']

    def extractFileUrls(self, response):
        res = []
        str_list = response.css('#BaseMainContent_MainContent_documentPanel input::attr(value)').extract()
        for link in str_list:
            if(len(json.loads(link)) == 0):
                continue;

            res.append('https://i.rts-tender.ru/main/FileServiceSite/FileDownloadHandler.ashx?FileGuid=' + json.loads(link)[0]['FileGuid'])

        return res



    def parse(self, response):
        self.log('I just visited: ' + response.url);
        yield{
            #ОСНОВНЫЕ СВЕДЕНИЯ
            'procedure_type' : response.css('#BaseMainContent_MainContent_fvNameByProcurementRegulations_lblValue::text').extract_first(),
            'procedure_number' : response.css('#BaseMainContent_MainContent_fvTradeNumber_lblValue::text').extract_first(),
            'procedure_name': response.css('#BaseMainContent_MainContent_fvName_lblValue::text').extract_first(),
            'seller': response.css('#BaseMainContent_MainContent_fvName_lblValue::text').extract_first(),

            #СВЕДЕНИЯ ОБ ОРГАНИЗАТОРЕ
            'organizer_name': response.css('#BaseMainContent_MainContent_fvOrganizer_lblValue::text').extract_first(),
            'full_organizer-name': response.css('#BaseMainContent_MainContent_fvOrganizerFullName_lblValue::text').extract_first(),
            'INN': response.css('#BaseMainContent_MainContent_fvOrganizerInn_lblValue::text').extract_first(),
            'KPP': response.css('#BaseMainContent_MainContent_fvOrganizerKpp_lblValue::text').extract_first(),
            'legal_adress': response.css('#BaseMainContent_MainContent_fvOrganizerAddress1_lblValue::text').extract_first(),
            'actual_adress': response.css('#BaseMainContent_MainContent_fvOrganizationAddress_lblValue::text').extract_first(),
            'email': response.css('#BaseMainContent_MainContent_fvOrganizerEmail_lblValue::text').extract_first(),
            'phone_number': response.css('#BaseMainContent_MainContent_fvOrganizationPhone_lblValue::text').extract_first(),

            #КОНТАКТНОЕ ЛИЦО
            'FIO': response.css('#BaseMainContent_MainContent_fvResponderFio_lblValue::text').extract_first(),
            'FIO_phone_number': response.css('#BaseMainContent_MainContent_fvResponderPhone_lblValue::text').extract_first(),
            'FIO_email': response.css('#BaseMainContent_MainContent_fvResponderEmail_lblValue::text').extract_first(),

            #ДОКУМЕНТЫ И СВЕДЕНИЯ
            'document': self.extractFileUrls(response),


            #Порядок оформления заявок на участие
            'demands' : response.css('#BaseMainContent_MainContent_fvParticipantRequirement_lblValue::text').extract_first(),
            'constraints': response.css('#BaseMainContent_MainContent_fvParticipantRequirement_lblValue::text').extract_first(),

            #Условия проведения процедуры
            'submission_form' : response.css('#BaseMainContent_MainContent_fvEscrapystatePriceApplicationType_lblValue::text').extract_first(),
            'submission_time_start' : response.css('#BaseMainContent_MainContent_ucTradeStageViewList_repStages_ucTradeStageView_0_fvApplicationStartDate_0_lblValue_0::text').extract_first(),
            'submission_time_end': response.css('#BaseMainContent_MainContent_ucTradeStageViewList_repStages_ucTradeStageView_0_fvApplicationEndDate_0_lblValue_0::text').extract_first(),
            'time_left' : response.css('#BaseMainContent_MainContent_ucTradeStageViewList_repStages_ucTradeStageView_0_fvApplicationEndDateDelay_0_lblValue_0::text').extract_first(),
            'place_to_show_documentation' : response.css('#BaseMainContent_MainContent_ucTradeStageViewList_repStages_ucTradeStageView_0_fvDocumentationPlace_0_lblValue_0::text').extract_first(),
            'review_date' : response.css('#BaseMainContent_MainContent_ucTradeStageViewList_repStages_ucTradeStageView_0_fvConsiderationDate_0_lblValue_0   ::text').extract_first(),
            'trading_start_time' : response.css('#BaseMainContent_MainContent_fvAuctionBeginDate_lblValue::text').extract_first(),
            'final_time' : response.css('#BaseMainContent_MainContent_fvResultDate_lblValue::text').extract_first(),

            #

        }




