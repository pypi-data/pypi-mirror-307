<?xml version="1.0"?>
<!-- Schematron rules for DBNL PDFs -->

<s:schema xmlns:s="http://purl.oclc.org/dsdl/schematron">

<s:pattern>
    <s:title>DBNL profile checks</s:title>

    <!-- Checks at PDF metadata level -->
    <s:rule context="/properties/meta">
        <!-- Check on PDF version -->
        <s:assert test="(format = 'PDF 1.7')">Unexpected PDF version (expected: 1.7)</s:assert>
        <!-- Check on encryption -->
        <s:assert test="(encryption = 'None')">PDF uses encryption</s:assert>
    </s:rule>

    <!-- Checks at page level -->
    <s:rule context="/properties/pages/page">
        <!-- Check on presence of only 1 image for each page -->
        <s:assert test="(count(image) = 1)">Unexpected number of images on page (expected: 1)</s:assert> 
    </s:rule>

    <!-- Checks at PDF object level -->
    <s:rule context="/properties/pages/page/image/pdf">
        <!-- Check on expected filter value for JPEG encoded image data -->
        <s:assert test="(filter = 'DCTDecode')">Unexpected filter value (expected: DCTDecode)</s:assert>
    </s:rule>

    <!-- Checks at image stream level -->
    <s:rule context="/properties/pages/page/image/stream">
        <!-- Check on expected format of the image stream -->
        <s:assert test="(format = 'JPEG')">Unexpected image stream format (expected: JPEG)</s:assert>
        <!-- Check on horizontal and vertical resolution (with tolerance of +/- 1 ppi) -->
        <s:assert test="(jfif_density_x &gt;= 299) and
        (jfif_density_x &lt;= 301)">Horizontal resolution outside permitted range</s:assert>
        <s:assert test="(jfif_density_y &gt;= 299) and
        (jfif_density_y &lt;= 301)">Vertical resolution outside permitted range</s:assert>
        <!-- Check on expected number of color components -->
        <s:assert test="(components = '3')">Unexpected number of color components (expected: 3)</s:assert>
        <!-- Check on JPEG compression quality level (with tolerance of +/- 2 levels) -->
        <s:assert test="(JPEGQuality &gt;= 83) and
        (JPEGQuality &lt;= 87)">JPEG compression quality outside permitted range</s:assert>
    </s:rule>

    <!-- Checks at combined PDF object and image stream levels -->
    <s:rule context="/properties/pages/page/image">
        <!-- Check on presence of ICC profile, which can be embedded as a PDF object, in the JPEG image stream, or both -->
        <s:assert test="(pdf/colorspace = 'ICCBased') or (stream/icc_profile)">Missing embedded ICC profile</s:assert>
        <!-- Consistency checks on width, height values at pdf and image stream levels -->
        <s:assert test="(pdf/width = stream/width)">Width values at PDF and image stream levels are not the same</s:assert>
        <s:assert test="(pdf/height = stream/height)">Height values at PDF and image stream levels are not the same</s:assert>
        <!-- Consistency check on bpc values at pdf and image stream levels -->
        <s:assert test="(pdf/bpc = stream/bpc)">Bit per component values at PDF and image stream levels are not the same</s:assert>
    </s:rule>

    <!-- Checks at properties level -->
    <s:rule context="/properties">
        <!-- Check on PageMode value to ensure document doesn't open with thumbnails -->
        <s:assert test="(PageMode  != '/UseThumbs')">PageMode value is /UseThumbs</s:assert>
        <!-- Check on signatureFlag value to ensure document doesn't contain digital signatures -->
        <s:assert test="(signatureFlag  = -1)">Document contains one or more digital signatures</s:assert>
    </s:rule>

    <!-- Checks at errors level -->
    <s:rule context="/properties/errors">
        <!-- Check on absence of any errors -->
        <s:assert test="(count(error) = 0)">Properties extraction resulted in one or more unexpected errors</s:assert>
    </s:rule>

    <!-- Checks at warnings level -->
    <s:rule context="/properties/warnings">
        <!-- Check on absence of any errors -->
        <s:assert test="(count(warning) = 0)">Properties extraction resulted in one or more warnings</s:assert>
    </s:rule>

</s:pattern>
</s:schema>