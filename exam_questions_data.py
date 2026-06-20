"""Curated multiple-choice questions — 1e zit reconstructie + exam-style oefenvragen."""

EXAM_SECTION_RECON = "1e zit 2025-2026"
EXAM_SECTION_SUPP = "Oefenvragen (examstijl)"


def _q(id_: str, section: str, question: str, options: list[str], correct: int) -> dict:
    return {
        "id": id_,
        "section": section,
        "q": question,
        "options": options,
        "correct": correct,
    }


# --- 1e zit 2025-2026 (studentenreconstructie) ---
RECONSTRUCTION_QUESTIONS = [
    _q(
        "ez-001", EXAM_SECTION_RECON,
        "Wat is een correcte uitspraak over de balkmetafoor (kwetsbaarheid-stressmodel)?",
        [
            "De stressoren liggen op de balk; de breedte van de balk is voor iedereen universeel hetzelfde.",
            "De balk staat voor kwetsbaarheid (diathese), gevormd door genetische en omgevingsfactoren; stressoren belasten de balk.",
            "Als de balk barst, mag de psychologisch consulent zelf behandelen zonder doorverwijzing.",
            "De metafoor werd ontwikkeld om vooral psychose te verklaren en heeft geen bredere toepassing.",
        ],
        1,
    ),
    _q(
        "ez-002", EXAM_SECTION_RECON,
        "Welke drie elementen vormen het Sense of Coherence-model (Antonovsky)?",
        [
            "Begrijpbaarheid, hanteerbaarheid en betekenisvolheid.",
            "Intimiteit, passie en toewijding.",
            "Aandacht, reactie en betekenis.",
            "Positieve emoties, betrokkenheid en relaties.",
        ],
        0,
    ),
    _q(
        "ez-003", EXAM_SECTION_RECON,
        "Een kind van 6 jaar met autisme verliest zijn moeder. Welke digitale tool past het best bij rouwondersteuning voor jongeren?",
        [
            "a-buddy.be (lotgenotencontact bij adoptie).",
            "missingyou.be (rouw bij jongeren en jongvolwassenen).",
            "bovendewolken.be (foto's en ondersteuning rond sterrenkinderen).",
            "geluksdriehoek.be (werken aan geluk: zijn, voelen, omringd).",
        ],
        1,
    ),
    _q(
        "ez-004", EXAM_SECTION_RECON,
        "Volgens Portzky (palliatief palet) en herstel na stress: welke fase is het meest optimaal om in te investeren voor herstel?",
        [
            "Drive en spanning (hyperarousal).",
            "Onderprikkeling en comfort (langdurig freeze).",
            "Ontspanning (positieve palliatieve activiteiten).",
            "Comfort alleen, zonder ooit activiteit te hervatten.",
        ],
        2,
    ),
    _q(
        "ez-005", EXAM_SECTION_RECON,
        "Casus: een vrouw ervaart veel druk op het werk; alles wordt aan haar gevraagd. Ze twijfelt om hulp te vragen. Volgens Lazarus is welk beoordelingspatroon het meest waarschijnlijk?",
        [
            "Primaire beoordeling: irrelevant; secundaire: voldoende hulpbronnen.",
            "Primaire beoordeling: bedreigend; secundaire: voldoende hulpbronnen maar ze zet ze niet in.",
            "Primaire beoordeling: bedreigend; secundaire: onvoldoende hulpbronnen om ermee om te gaan.",
            "Primaire beoordeling: uitdaging; secundaire: geen coping nodig.",
        ],
        2,
    ),
    _q(
        "ez-006", EXAM_SECTION_RECON,
        "Door welke factoren wordt de impact van een life event vooral bepaald (subjectieve benadering)?",
        [
            "Alleen de objectieve ernst van de gebeurtenis op de SRRS-schaal.",
            "Levensgeschiedenis, persoonseigenschappen, hechtingsstijl en gezondheidstoestand.",
            "Uitsluitend genetische aanleg, onafhankelijk van interpretatie.",
            "Enkel het macrosysteem en beleid, niet het individu.",
        ],
        1,
    ),
    _q(
        "ez-007", EXAM_SECTION_RECON,
        "Welke uitspraak over siblingrelaties is correct volgens de cursus?",
        [
            "Stief- en halfbroers/-zussen hebben altijd minder conflict dan biologische siblings.",
            "Conflict is het hoogst in de eerste graad van het middelbaar onderwijs en neemt daarna toe.",
            "De siblingrelatie kan de langstdurende relatie zijn en blijft bestaan, ook bij weinig contact of zonder emotionele verbinding.",
            "Siblingrelaties bestaan uit exact vier types: harmonieus, conflictueus, afstandelijk en conflict-intens.",
        ],
        2,
    ),
    _q(
        "ez-008", EXAM_SECTION_RECON,
        "Welke uitspraak over de polyvagaal theorie is correct?",
        [
            "Het ventrale vagale systeem is evolutionair het oudste systeem in de hiërarchie.",
            "Het dorsale vagale systeem (onderdeel van het autonome zenuwstelsel) kan leiden tot freeze/fawn.",
            "De drie principes zijn hiërarchie, proprioceptie en dissociatie.",
            "Het ventrale systeem verhoogt cortisol en zorgt zo voor maximale alertheid.",
        ],
        1,
    ),
    _q(
        "ez-009", EXAM_SECTION_RECON,
        "Wat is géén wettelijke voorwaarde voor euthanasie bij een terminale, medisch uitzichtloze aandoening?",
        [
            "Raadpleging van een tweede arts.",
            "Vrijwillig, schriftelijk en duurzaam verzoek van de patiënt.",
            "Een verplichte wachttijd van één maand tussen verzoek en uitvoering.",
            "Ondraaglijk fysiek of psychisch lijden.",
        ],
        2,
    ),
    _q(
        "ez-010", EXAM_SECTION_RECON,
        "Artikel over ethische adolescenten en discriminatie: welke uitspraak is correct?",
        [
            "Vriendschappen met leeftijdsgenoten met een andere achtergrond bevorderen de ontwikkeling van adolescenten.",
            "Minstens één contact met iemand met een andere achtergrond hangt samen met minder ervaren discriminatie door leeftijdsgenoten én docenten.",
            "Discriminatie door leerkrachten heeft hetzelfde effect op schoolprestaties als discriminatie door medestudenten.",
            "Diversiteit in vriendschappen heeft geen invloed op latere welzijn.",
        ],
        1,
    ),
    _q(
        "ez-011", EXAM_SECTION_RECON,
        "Een man werkt al 20 jaar bij dezelfde werkgever en ervaart veel stress. Waar kan hij als psychologisch consulent het best naar doorverwijzen?",
        [
            "noknok.be (jongeren 12–16 jaar).",
            "geluksdriehoek.be (psycho-educatie rond geluk: zijn, voelen, omringd).",
            "veerkrachtverhalen.be (verhalen over veerkracht).",
            "overkop.be (crisisopvang jongeren).",
        ],
        1,
    ),
    _q(
        "ez-012", EXAM_SECTION_RECON,
        "Een man (28 jaar) identificeert zich als transgender en zoekt ondersteuning. Waar kan hij terecht?",
        [
            "Casa Rosa (gespecialiseerde ondersteuning rond genderdiversiteit).",
            "noknok.be (jongeren 12–16 jaar).",
            "pimento.be (pesten).",
            "allesoverpesten.be (slachtoffers van pesten).",
        ],
        0,
    ),
    _q(
        "ez-013", EXAM_SECTION_RECON,
        "Welke stelling over perinatale gezondheid is correct?",
        [
            "De culturele achtergrond van de moeder beïnvloedt hoe zij met postnatale depressie omgaat, wat effect heeft op het kind.",
            "Psychische problemen komen in de perinatale fase zelden voor (< 1 op 20).",
            "Postnatale depressie treft uitsluitend biologische moeders, niet partners.",
            "Baby blues zijn een ernstige psychiatrische stoornis die altijd medicatie vereist.",
        ],
        0,
    ),
    _q(
        "ez-014", EXAM_SECTION_RECON,
        "Welke term beschrijft het proces van ouder worden met identiteitsvorming, vergelijkbaar met de adolescentie?",
        [
            "Matrescentie (voor moeders) / patrescentie (voor vaders).",
            "Parentificatie (kind neemt ouderrol op).",
            "Ouderidentificatie (identificatie met eigen ouders).",
            "Transitie-aanpassing (alleen gedragsaanpassing, geen identiteit).",
        ],
        0,
    ),
    _q(
        "ez-015", EXAM_SECTION_RECON,
        "Welke stelling over grootouder worden is correct?",
        [
            "Grootouders worden vandaag gemiddeld méér gevraagd dan 20 jaar geleden, zonder spanning.",
            "Er bestaat een spanningsveld tussen betrokkenheid bij het jonge gezin en het bewaren van eigen autonomie.",
            "Hoe vaak grootouders hun kleinkind zien, heeft geen invloed op hoe betrokken ze willen zijn.",
            "Grootouders hebben wettelijk de hoofdverantwoordelijkheid voor de opvoeding.",
        ],
        1,
    ),
    _q(
        "ez-016", EXAM_SECTION_RECON,
        "Welke drie componenten vormen Sternbergs triangulatietheorie van liefde?",
        [
            "Intimiteit, passie en toewijding (commitment).",
            "Intimiteit, vertrouwen en passie.",
            "Vertrouwen, passie en engagement.",
            "Hechting, genegenheid en loyaliteit.",
        ],
        0,
    ),
    _q(
        "ez-017", EXAM_SECTION_RECON,
        "Welke uitspraak over subjectief welbevinden (SWB) is correct?",
        [
            "Een hoger SWB gaat altijd samen met verminderde academische resultaten.",
            "Volgens de affectieve theorie kunnen life events SWB op lange termijn beïnvloeden.",
            "Extreem hoog SWB is altijd beter dan matig positief SWB.",
            "De set-point theorie stelt dat life events permanent SWB verhogen.",
        ],
        1,
    ),
    _q(
        "ez-018", EXAM_SECTION_RECON,
        "Bij welk type racisme hoort de uitspraak: 'Hij is alleen aangenomen omdat hij van dat ras is'?",
        [
            "Structureel racisme (institutioneel beleid).",
            "Micro-agressie: micro-invalidatie.",
            "Micro-agressie: micro-belediging.",
            "Macro-agressie: fysiek geweld.",
        ],
        2,
    ),
    _q(
        "ez-019", EXAM_SECTION_RECON,
        "Wat is een kernidee van het Integratief Procesmodel (IPM) van rouw?",
        [
            "Rouw verloopt lineair in vijf vaste fasen bij iedereen.",
            "Existentiële spanningen en thema's (bv. dood accepteren, leven omarmen) spelen een centrale rol.",
            "Rouw is uitsluitend een fysieke dimensie zonder cognitieve component.",
            "Gecompliceerde rouw komt bij minder dan 1% van de mensen voor.",
        ],
        1,
    ),
    _q(
        "ez-020", EXAM_SECTION_RECON,
        "Welke stelling over het PERMA-model (Seligman) is fout?",
        [
            "PERMA hangt samen met subjectief welbevinden.",
            "PERMA bestaat uit vier componenten.",
            "Negatieve emoties kunnen soms functioneel zijn.",
            "PERMA omvat onder meer betekenis (Meaning) en prestatie (Achievement).",
        ],
        1,
    ),
    _q(
        "ez-021", EXAM_SECTION_RECON,
        "Een leerkracht wil pesten in de klas aanpakken. Welke tool past het best?",
        [
            "pimento.be (hulpverleners en pesten).",
            "moodspace.be (studentenwelzijn).",
            "bovendewolken.be (foto's sterrenkinderen).",
            "druglijn.be/grip (KOPP-kinderen).",
        ],
        0,
    ),
    _q(
        "ez-022", EXAM_SECTION_RECON,
        "Artikel over ouderen en rouwen: welke uitspraak is correct?",
        [
            "Ouderen ervaren bij rouw eenzaamheid; LGBTQ-vrouwen en oudere vrouwen voelen vaker isolatie.",
            "Rouw bij ouderen heeft nooit invloed op fysieke gezondheid.",
            "Ouderen rouwen altijd sneller dan jongere volwassenen.",
            "Professionele hulp is bij ouderenrouw contraproductief.",
        ],
        0,
    ),
    _q(
        "ez-023", EXAM_SECTION_RECON,
        "Welke uitspraak over het kwetsbaarheid-stressmodel is correct?",
        [
            "Het model werd oorspronkelijk ontwikkeld in onderzoek naar psychotische episodes (Zubin & Spring).",
            "Stress alleen is voldoende om psychopathologie te verklaren.",
            "Kwetsbaarheid en risicofactor zijn exact hetzelfde begrip.",
            "Coping is aangeboren en niet trainbaar.",
        ],
        0,
    ),
    _q(
        "ez-024", EXAM_SECTION_RECON,
        "Een transgender persoon heeft negatieve gevoelens tegenover zichzelf. Welke proximale factor is dit?",
        [
            "Geïnternaliseerde transfobie.",
            "Non-affirmatie door de omgeving.",
            "Non-disclosure (niet out zijn).",
            "Externe victimisatie (uitsluitend fysiek geweld).",
        ],
        0,
    ),
    _q(
        "ez-025", EXAM_SECTION_RECON,
        "Welke uitspraak over het AREA-model (Wilson & Gilbert) is correct?",
        [
            "AREA staat voor: Aandacht, Reactie, Externe factoren, Aanhouden.",
            "Betekenisgeving is cruciaal in dit model voor het vormen van veerkracht.",
            "Het model stelt dat appraisals geen rol spelen bij life events.",
            "AREA vervangt volledig het kwetsbaarheid-stressmodel.",
        ],
        1,
    ),
    _q(
        "ez-026", EXAM_SECTION_RECON,
        "Volgens het transgender-hoofdstuk (chapter 18): welke aanbeveling is correct rond chirurgie?",
        [
            "Rookstop moet worden ingelast vóór genderbevestigende chirurgie.",
            "Conversietherapie moet standaard worden aangeraden.",
            "Psychotherapie is altijd verplicht vóór elke hormoonbehandeling.",
            "Een verplichte hormoonstop van één jaar is wettelijk voorgeschreven.",
        ],
        0,
    ),
    _q(
        "ez-027", EXAM_SECTION_RECON,
        "Iemand werkt in een job onder zijn/haar diploma-niveau. Hoe heet dit in arbeidsmarktterminologie?",
        [
            "Ondertewerkstelling (niveau onder tewerkstelling).",
            "Overwerkstelling (meer verantwoordelijkheid dan diploma).",
            "Domein-tewerkstelling (andere sector dan opleiding).",
            "Structurele werkloosheid.",
        ],
        0,
    ),
    _q(
        "ez-028", EXAM_SECTION_RECON,
        "Welke uitspraak over baby blues is correct?",
        [
            "Baby blues duren typisch tot ongeveer de zesde week na de bevalling en zijn geen psychiatrische stoornis.",
            "Baby blues treffen minder dan 5% van de moeders.",
            "Baby blues vereisen altijd opname op een psychiatrische afdeling.",
            "Baby blues en postnatale depressie zijn hetzelfde.",
        ],
        0,
    ),
    _q(
        "ez-029", EXAM_SECTION_RECON,
        "Artikel over pesten (Pabian e.a.): welke uitspraak is correct?",
        [
            "De subjectieve ervaring van pesten heeft invloed op mentale gezondheid op lange termijn.",
            "Pesten in de kindertijd heeft geen effect meer na het 18de levensjaar.",
            "Alleen fysiek pesten telt mee; relationeel pesten niet.",
            "Pesten beïnvloedt uitsluitend schoolcijfers, niet welzijn.",
        ],
        0,
    ),
    _q(
        "ez-030", EXAM_SECTION_RECON,
        "Artikel over burn-out bij studenten: wat is een belangrijk risicofactor?",
        [
            "Overmatig internetgebruik.",
            "Hoge intrinsieke motivatie zonder stress.",
            "Regelmatige lichaamsbeweging.",
            "Sterk sociaal netwerk op campus.",
        ],
        0,
    ),
    _q(
        "ez-031", EXAM_SECTION_RECON,
        "Wat is palliatieve zorg?",
        [
            "Een holistische benadering die kwaliteit van leven verbetert door vroegtijdige herkenning en behandeling van lijden (fysiek, psychosociaal, spiritueel).",
            "Een zorgtraject dat pas start als alle curatieve behandelingen zijn stopgezet.",
            "Uitsluitend pijnbestrijding zonder aandacht voor psychosociale aspecten.",
            "Behandeling die als doel heeft de dood te bespoedigen.",
        ],
        0,
    ),
    _q(
        "ez-032", EXAM_SECTION_RECON,
        "Welke factoren droegen bij aan veerkracht bij zowel jonge vluchtelingen in Ethiopië als bij migranten in Europa (cursus)?",
        [
            "Sociale contacten, bijdragen aan de maatschappij en betaald werk.",
            "Uitsluitend contact met het thuisland.",
            "Alleen school, zonder sociale steun.",
            "Vrijwilligerswerk alleen, zonder werk of school.",
        ],
        0,
    ),
    _q(
        "ez-033", EXAM_SECTION_RECON,
        "Een vrouw van 80 woont in Gent en heeft weinig sociale contacten. Waar kan ze terecht voor sociale ondersteuning?",
        [
            "Rits Artevelde (sociale contacten voor ouderen in de regio).",
            "noknok.be (jongeren 12–16 jaar).",
            "moodspace.be (studentenwelzijn).",
            "pimento.be (pesten).",
        ],
        0,
    ),
    _q(
        "ez-034", EXAM_SECTION_RECON,
        "Na de dood van zijn vader wil een jongen gaan basketten en lijkt minder verdrietig dan moeder en zus. Wat is correct?",
        [
            "Dit is een normale reactie: kinderen zijn niet continu bezig met verlies en zoeken ook afleiding.",
            "Dit wijst altijd op pathologische ontkenning en vereist direct crisisopvang.",
            "Kinderen mogen pas spelen na minstens één jaar rouw.",
            "Kinderen voelen nooit verdriet bij het verlies van een ouder.",
        ],
        0,
    ),
    _q(
        "ez-035", EXAM_SECTION_RECON,
        "Welk rouwpatroon kwam het meest voor bij mensen die hun partner verloren (Bonanno et al.)?",
        [
            "Chronische rouw (langdurige intense rouw bij iedereen).",
            "Een stabiel patroon van relatief lage depressie met veerkracht (resilience).",
            "Klassieke rouw: eerst een dip, daarna geleidelijk herstel bij iedereen.",
            "Uitgestelde rouw (delayed grief) bij de meerderheid.",
        ],
        1,
    ),
    _q(
        "ez-036", EXAM_SECTION_RECON,
        "Artikel over ouderen en rouwen: welke bijkomende uitspraak is correct?",
        [
            "Door rouw kunnen meer gezondheidsproblemen ontstaan.",
            "Rouw beschermt altijd tegen fysieke klachten.",
            "Ouderen hebben geen behoefte aan sociale steun bij verlies.",
            "Rouw bij ouderen is altijd kortdurend (< 2 weken).",
        ],
        0,
    ),
    _q(
        "ez-037", EXAM_SECTION_RECON,
        "Welke uitspraak over het AREA-model is eveneens correct?",
        [
            "Betekenisgeving kan worden beïnvloed door persoonlijke attributies en omgevingsfactoren.",
            "Het model stelt dat externe factoren geen rol spelen bij appraisals.",
            "AREA betekent: Aandacht, Reactie, Emotie, Aanpassing.",
            "Het model werd ontwikkeld door Antonovsky.",
        ],
        0,
    ),
    _q(
        "ez-038", EXAM_SECTION_RECON,
        "Een psychologisch consulent mag bij complexe rouw bij een kind met autisme niet alles alleen. Wat is de juiste eerste stap?",
        [
            "Doorverwijzen naar gespecialiseerde hulp naast eventuele digitale ondersteuning (bv. missingyou.be).",
            "Zelf langdurige traumatherapie starten zonder overleg.",
            "Afwachten tot het kind zelf hulp vraagt.",
            "Het kind doorsturen naar geluksdriehoek.be.",
        ],
        0,
    ),
]

# --- Aanvullende oefenvragen in dezelfde examstijl ---
SUPPLEMENTARY_QUESTIONS = [
    _q(
        "sup-001", "Hoorcollege 1: Inleiding",
        "Welke uitspraak over de balkmetafoor en draaglast/draagkracht is juist?",
        [
            "Draaglast = stressoren; draagkracht = coping, steun en energie.",
            "Draaglast = genetica; draagkracht = stressoren.",
            "Als draaglast gelijk is aan draagkracht ontstaat altijd psychopathologie.",
            "De metafoor meet stress uitsluitend met de SRRS.",
        ],
        0,
    ),
    _q(
        "sup-002", "Hoorcollege 1: Inleiding",
        "Wanneer ontstaat stress volgens Lazarus?",
        [
            "Bij elke life event, ongeacht beoordeling.",
            "Wanneer de situatie als bedreigend/belangrijk wordt beoordeeld én iemand onvoldoende hulpbronnen heeft.",
            "Alleen bij catastrofes, niet bij dagelijkse ergernissen.",
            "Uitsluitend wanneer de primaire beoordeling 'uitdaging' is.",
        ],
        1,
    ),
    _q(
        "sup-003", "Hoorcollege 1: Inleiding",
        "Welke volgorde in de polyvagaal hiërarchie is correct (van meest adaptief naar minst adaptief)?",
        [
            "Ventral vagale → sympathisch → dorsaal vagale.",
            "Dorsaal vagale → sympathisch → ventral vagale.",
            "Sympathisch → dorsaal vagale → ventral vagale.",
            "Ventral vagale → dorsaal vagale → sympathisch.",
        ],
        0,
    ),
    _q(
        "sup-004", "Hoorcollege 2: Ouderschap",
        "Wat is het verschil tussen baby blues en postnatale depressie?",
        [
            "Baby blues: kortdurend (dagen tot ~6 weken), geen stoornis; postnatale depressie: minstens 2 weken, klinisch relevant.",
            "Baby blues treft 1 op 20 moeders; postnatale depressie is zeldzamer.",
            "Baby blues vereist antidepressiva; postnatale depressie niet.",
            "Er is geen verschil; het zijn synoniemen.",
        ],
        0,
    ),
    _q(
        "sup-005", "Hoorcollege 2: Ouderschap",
        "Wat is parentificatie?",
        [
            "Een kind neemt (te vroeg) ouderlijke taken of zorg voor ouders/broers/zussen op.",
            "De transitie naar ouderschap met identiteitsheroriëntatie.",
            "Het verlies van een kind tijdens zwangerschap.",
            "Wettelijke adoptie door grootouders.",
        ],
        0,
    ),
    _q(
        "sup-006", "Hoorcollege 3: Relaties",
        "Welke liefdesvorm hoort bij intimiteit + passie volgens Sternberg?",
        [
            "Romantische liefde.",
            "Lege liefde.",
            "Sociale liefde / gezelschap.",
            "Volmaakte liefde.",
        ],
        0,
    ),
    _q(
        "sup-007", "Hoorcollege 3: Relaties",
        "Wat is seksisme volgens de cursus?",
        [
            "Gedrag waarbij iemand of een groep wordt gediscrimineerd op basis van geslacht.",
            "Elke vorm van ongelijkheid, ongeacht criterium.",
            "Uitsluitend fysiek geweld tegen vrouwen.",
            "Het verschil tussen sekse en gender.",
        ],
        0,
    ),
    _q(
        "sup-008", "Hoorcollege 3: Relaties",
        "Is transgender zijn een psychische aandoening volgens de gendermodule?",
        [
            "Nee; hogere psychische klachten hangen samen met minority stress.",
            "Ja; het staat in DSM-5 als primaire diagnose.",
            "Ja; psychotherapie is altijd verplicht vóór elke zorg.",
            "Nee; transgender personen hebben nooit psychische klachten.",
        ],
        0,
    ),
    _q(
        "sup-009", "Hoorcollege 4: School & Werk",
        "Welke tool is een aanrader voor studentenwelzijn in de examenperiode?",
        [
            "moodspace.be",
            "bovendewolken.be",
            "waarblijftmijntijd.mantelzorg.nl",
            "vaderen.be",
        ],
        0,
    ),
    _q(
        "sup-010", "Hoorcollege 4: School & Werk",
        "Wat toonde het longitudinale pesten-onderzoek (Britse cohort)?",
        [
            "Gepeste kinderen (7–11 jaar) hadden op 50-jarige leeftijd nog meer depressie en lagere levenskwaliteit.",
            "Pesten heeft geen effect na het verlaten van de lagere school.",
            "Alleen meisjes worden langdurig beïnvloed door pesten.",
            "Pesten verhoogt uitsluitend angst, niet depressie.",
        ],
        0,
    ),
    _q(
        "sup-011", "Hoorcollege 5: Verlies",
        "Welk rouwpatroon werd amper gevonden door Bonanno et al.?",
        [
            "Delayed grief (uitgestelde rouw).",
            "Resilience (veerkracht).",
            "Common grief.",
            "Chronic depression.",
        ],
        0,
    ),
    _q(
        "sup-012", "Hoorcollege 5: Verlies",
        "Wat is géén wettelijke voorwaarde voor euthanasie?",
        [
            "Een verplichte wachttijd van één maand bij een terminale aandoening.",
            "Wilsbekwaamheid van de patiënt.",
            "Ondraaglijk lijden.",
            "Schriftelijk verzoek (voor meerderjarigen).",
        ],
        0,
    ),
    _q(
        "sup-013", "Hoorcollege 6: Omgaan met Life Events",
        "Wat betekent AREA?",
        [
            "Attent → React → Explain → Adapt.",
            "Aandacht, Reactie, Emotie, Aanpassing.",
            "Appraisal, Resilience, Emotie, Acceptatie.",
            "Aanvaarden, Rouwen, Evalueren, Aanpassen.",
        ],
        0,
    ),
    _q(
        "sup-014", "Hoorcollege 6: Omgaan met Life Events",
        "Wat is het palliatief palet (Portzky)?",
        [
            "Alle activiteiten om stress/negatieve gevoelens tijdelijk te verminderen; van positief tot destructief.",
            "Alleen medicamenteuze pijnbestrijding in palliatieve zorg.",
            "Een lijst van toegestane euthanasie-indicaties.",
            "Het verschil tussen rouw en depressie.",
        ],
        0,
    ),
    _q(
        "sup-015", "Hoorcollege 6: Omgaan met Life Events",
        "Wat stelt het Dual Process Model (DPM) van rouw?",
        [
            "Afwisseling tussen verliesgerichte en herstelgerichte coping.",
            "Rouw verloopt strikt lineair in vijf fasen.",
            "Rouw duurt maximaal zes maanden.",
            "Herstel betekent volledig vergeten van de overledene.",
        ],
        0,
    ),
    _q(
        "sup-016", "Digitale Tools",
        "Welke tool past bij foto's van sterrenkinderen na perinataal verlies?",
        [
            "bovendewolken.be",
            "missingyou.be",
            "geluksdriehoek.be",
            "a-buddy.be",
        ],
        0,
    ),
    _q(
        "sup-017", "Digitale Tools",
        "Waarvoor dient perinatalehulp.be/zelfhulp?",
        [
            "Zelfhulptraject bij depressie na zwangerschap (~10 weken).",
            "Crisisopvang voor jongeren 12–16 jaar.",
            "Pesten in het secundair onderwijs.",
            "Burn-out bij zorgverleners.",
        ],
        0,
    ),
    _q(
        "sup-018", "Hoorcollege 1: Inleiding",
        "Welke beperking van de SRRS (Holmes & Rahe) is correct?",
        [
            "Subjectieve interpretatie en culturele context worden niet meegenomen.",
            "De schaal meet alleen dagelijkse ergernissen.",
            "De schaal is alleen geldig voor kinderen.",
            "De schaal houdt geen rekening met cumulatie van events.",
        ],
        0,
    ),
    _q(
        "sup-019", "Hoorcollege 3: Relaties",
        "Wat toonde de Jane Elliott blue eyes/brown eyes-oefening?",
        [
            "Vooroordelen kunnen snel ontstaan; wie discriminatie ondervond, discrimineert minder snel zelf.",
            "Discriminatie is alleen biologisch bepaald.",
            "Kinderen hebben geen in-group voorkeur.",
            "Racisme is uitsluitend bewust en opzettelijk.",
        ],
        0,
    ),
    _q(
        "sup-020", "Hoorcollege 5: Verlies",
        "Wat zijn bronnen van veerkracht bij jonge vluchtelingen in Ethiopië?",
        [
            "Sociale steun, school, werk en zinvolle activiteiten.",
            "Uitsluitend religie, zonder sociale contacten.",
            "Isolatie van de lokale gemeenschap.",
            "Vermijden van onderwijs om stress te verlagen.",
        ],
        0,
    ),
]


def all_exam_questions() -> list[dict]:
    return RECONSTRUCTION_QUESTIONS + SUPPLEMENTARY_QUESTIONS
