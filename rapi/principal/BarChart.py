"Multi-line x-axis labels"
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String, Line
from reportlab.lib.colors import purple, PCMYKColor, red, Color, CMYKColor, black
from reportlab.graphics.charts.textlabels import Label

class BarChart04(_DrawingEditorMixin,Drawing):
    '''
        Chart Features
        --------------
        This drawing demonstrates the ability to add multi row text to the X Axis in the chart.
        It also features a long ticks which looks more like a table:

        - The ticks are controlled with the property **chart.categoryAxis.tickDown=36**

        This chart was built with our [Diagra](http://www.reportlab.com/software/diagra/) solution.

        Not the kind of chart you looking for? Go [up](..) for more charts, or to see different types of charts click on [ReportLab Charts Gallery](/chartsgallery/).
    '''
    def __init__(self,width=400,height=200,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
        self._add(self,Label(),name='YLabel',validate=None,desc="The label on the vertical axis")
        self._add(self,Label(),name ='XLabel',validate=None,desc="The label on the horizontal axis")
        # font
        fontName = 'Helvetica'
        strokeWidth = 0.5
        strokeDashArray = (0.3, 1) #, 0.25
        lineCap = 1
        gridStickOut = 4
        tickOut     = 36
        self.chart.barSpacing = 3
        self.chart.barWidth = 9
        self.chart.groupSpacing = 15
        self.chart.width = 319
        self.chart.x = 24
        self.chart.y = 54
        self.chart.bars.strokeColor = None
        self.chart.bars.strokeWidth = 0
        # colour list can read its colours from the palette
        colorsList = [PCMYKColor(100,60,0,50,alpha=100), PCMYKColor(100,0,90,50,alpha=100)]
        for i, color in enumerate(colorsList): self.chart.bars[i].fillColor = colorsList[i]
        self.chart.categoryAxis.joinAxisMode='bottom'
        self.chart.categoryAxis.labelAxisMode='low'
        self.chart.categoryAxis.labels.angle = 0
        self.chart.categoryAxis.labels.boxAnchor = 'n'
        self.chart.categoryAxis.labels.dy = -4
        self.chart.categoryAxis.labels.fillColor = black
        self.chart.categoryAxis.labels.fontName = fontName
        self.chart.categoryAxis.labels.fontSize = 6
        self.chart.categoryAxis.labels.textAnchor='middle'
        self.chart.categoryAxis.tickShift=0
        self.chart.categoryAxis.visibleTicks = 1
        self.chart.categoryAxis.tickDown    = tickOut
        self.chart.categoryAxis.strokeDashArray      = strokeDashArray
        self.chart.categoryAxis.strokeWidth         = strokeWidth
        self.chart.categoryAxis.gridStrokeWidth     = strokeWidth
        self.chart.categoryAxis.visibleGrid         = 0
        self.chart.categoryAxis.gridStrokeDashArray = strokeDashArray
        self.chart.valueAxis.labels.fontName = fontName
        self.chart.valueAxis.labels.fontSize = 6
        self.chart.valueAxis.labels.rightPadding   = 3
        self.chart.valueAxis.drawGridLast=1
        self.chart.valueAxis.rangeRound='both'
        #self.chart.valueAxis.valueStep = 5
        self.chart.valueAxis.minimumTickSpacing    = 0.5
        self.chart.valueAxis.maximumTicks          = 8
        self.chart.valueAxis.forceZero             = 1
        self.chart.valueAxis.avoidBoundFrac = None
        self.chart.valueAxis.gridStrokeDashArray = strokeDashArray
        self.chart.valueAxis.visibleGrid = 1
        self.chart.valueAxis.gridStrokeWidth       = strokeWidth
        self.chart.valueAxis.strokeDashArray       = strokeDashArray
        self.chart.valueAxis.strokeWidth           = strokeWidth
        self.chart.valueAxis.gridStart              = self.chart.x-gridStickOut
        self.chart.valueAxis.gridEnd                = self.chart.x+self.chart.width+gridStickOut
        self.chart.valueAxis.gridStrokeLineCap      = lineCap
        self.chart.valueAxis.visibleTicks           = False
        self.chart.valueAxis.strokeColor            = None
        # self.legend.alignment = 'right'
        # self.legend.autoXPadding = 6
        # self.legend.boxAnchor = 'sw'
        # self.legend.columnMaximum = 1
        # self.legend.dx = 7
        # self.legend.dxTextSpace = 2
        # self.legend.dy = 7
        # self.legend.fontSize = 6
        # self.legend.strokeColor = None
        # self.legend.strokeWidth = 0
        # self.legend.subCols.minWidth = 55
        # self.legend.variColumn = 1
        # self.legend.x = 26
        # self.legend.y = -12
        # self.legend.fontName = fontName
        self.XLabel._text = ""
        self.XLabel.fontSize = 6
        self.XLabel.height = 0
        self.XLabel.maxWidth = 100
        self.XLabel.textAnchor ='middle'
        self.XLabel.x = 140
        self.XLabel.y = 10
        self.YLabel._text = ""
        self.YLabel.angle = 90
        self.YLabel.fontSize = 6
        self.YLabel.height = 0
        self.YLabel.maxWidth = 100
        self.YLabel.textAnchor ='middle'
        self.YLabel.x = 12
        self.YLabel.y = 80
        # 0 axis
        self.chart.annotations=[lambda c,cA,vA: Line(c.x,vA(0),c.x+c.width,vA(0),strokeColor=black,strokeWidth=strokeWidth)]
        # left vertical
        self.chart.annotations.extend([lambda c,cA,vA: Line(c.x,c.y-tickOut,c.x,self.chart.y+c.height+gridStickOut,strokeColor=black,strokeWidth=strokeWidth)])
        # right vertical
        self.chart.annotations.extend([lambda c,cA,vA: Line(c.x+c.width,c.y-tickOut,c.x+c.width,self.chart.y+c.height+gridStickOut,strokeColor=black,strokeWidth=0.5)])
        #self.chart.data = [[19.260000000000002, 32.359999999999999, 1.78, -4.3499999999999996, 2.1000000000000001, 5.1200000000000001, 11.0], [18.239999999999998, 14.85, -10.619999999999999, -7.8700000000000001, 0.90000000000000002, 2.5899999999999999, 10.869999999999999]]
        self.chart.categoryAxis.categoryNames = [u'Quarterly', u'YTD', u'1 Year', u'3 Year', u'5 Year', u'10 Year', u'Since Inception\n(11/05/1984)']
        colorsList= (PCMYKColor(100,60,0,50,alpha=100), PCMYKColor(100,0,90,50,alpha=100), PCMYKColor(80,24,69,70,spotName='350c',alpha=100), PCMYKColor(0,0,0,40,alpha=100), PCMYKColor(0,0,0,100,alpha=100))
        self.width       = 400
        self.height      = 200
        self.chart.width           = 350
        self.chart.height          = 125
        self.chart.bars[0].fillColor   = PCMYKColor(100,60,0,50,alpha=100)
        self.chart.bars[1].fillColor   = PCMYKColor(100,0,90,50,alpha=100)
        y = self.chart.y - 26
        colWidth = self.chart.width * 1.0 / len(self.chart.data[0])
        for i in xrange(len(self.chart.data)):
            self.chart.bars[i].fillColor = colorsList[i]
        # for h, series in enumerate(self.chart.data):
        #     for (i, value) in enumerate(series):
        #         if value is None:
        #             text = 'N/A'
        #         else:
        #             text = '%0.2f' % value
        #         x = self.chart.x + (i + 0.5) * colWidth
        #         s = String(x, y, text, textAnchor='middle')
        #         s.fontSize = 6
        #         s.fillColor =  self.chart.bars[h].fillColor
        #         self.add(s)
        #     y = y - 8
if __name__=="__main__": #NORUNTESTS
    BarChart04().save(formats=['pdf'],outDir='.',fnRoot=None)