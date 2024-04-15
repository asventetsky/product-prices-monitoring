import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { LineChart, axisClasses } from '@mui/x-charts';

import Title from './Title';


export default function Chart({ currentProductName, productPrices }) {

  const theme = useTheme();

  return (
    <React.Fragment>
      <Title>{currentProductName}</Title>
      <div style={{ width: '100%', flexGrow: 1, overflow: 'hidden' }}>
        <LineChart
          dataset={productPrices}
          margin={{
            top: 16,
            right: 20,
            left: 70,
            bottom: 30,
          }}
          xAxis={[
            {
              dataKey: 'date',
              scaleType: 'time',
              //               valueFormatter: (date) => (date != null || date != 0) ? date.toISOString().split('T')[0] : '',
            },
          ]}
          yAxis={[
            {
              label: 'Price (₺‎)',
              labelStyle: {
                ...theme.typography.body1,
                fill: theme.palette.text.primary,
              },
              tickLabelStyle: theme.typography.body2,
              max: productPrices.reduce((a, b) => a.price > b.price ? a : b, 0).price,
              tickNumber: 3,
            },
          ]}
          series={[
            {
              dataKey: 'price',
              showMark: false,
              color: theme.palette.primary.light,
              area: true,
            },
          ]}
          sx={{
            [`.${axisClasses.root} line`]: { stroke: theme.palette.text.secondary },
            [`.${axisClasses.root} text`]: { fill: theme.palette.text.secondary },
            [`& .${axisClasses.left} .${axisClasses.label}`]: {
              transform: 'translateX(-25px)',
            },
          }}
          grid={{ vertical: true, horizontal: true }}
        />
      </div>
    </React.Fragment>
  );
}
